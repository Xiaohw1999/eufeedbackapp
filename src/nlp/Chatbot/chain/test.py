from fastapi import FastAPI, HTTPException
import fitz  # PyMuPDF for PDF handling
import requests
import tempfile
import os
from langchain_openai import OpenAIEmbeddings
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from pymongo import MongoClient

# Load environment variables
api_key = os.getenv("OPENAI_API_KEY")
ATLAS_USER = os.getenv("ATLAS_USER")
ATLAS_TOKEN = os.getenv("ATLAS_TOKEN")

# FastAPI app initialization
app = FastAPI()

# MongoDB connection setup
client = MongoClient(f"mongodb+srv://{ATLAS_USER}:{ATLAS_TOKEN}@cluster0.mongodb.net/?retryWrites=true&w=majority")
db_name = "metadata"
collection_summary_name = "initiatives_summary_data"
initiatives_summary = client[db_name][collection_summary_name]

def download_pdf_to_tempfile(url):
    response = requests.get(url)
    response.raise_for_status()
    
    # create a temporary file to save the PDF
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    temp_file.write(response.content)
    temp_file.flush()
    temp_file.seek(0)
    
    return temp_file.name

def extract_text_from_pdf(file_path):
    document = fitz.open(file_path)
    text = ""
    
    # traverse each page and extract text
    for page_num in range(len(document)):
        page = document.load_page(page_num)
        text += page.get_text()
    
    return text

@app.post("/generate_summary/{initiative_id}")
async def generate_summary(initiative_id: str):
    initiative = initiatives_summary.find_one({"id": initiative_id}, {"_id": 0, "attachments": 1})
    
    # If initiative does not exist, return 404
    if not initiative:
        raise HTTPException(status_code=404, detail="Initiative not found.")
    
    # Get the first attachment
    attachments = initiative.get("attachments", [])
    if not attachments or len(attachments) == 0:
        raise HTTPException(status_code=404, detail="No attachments found for this initiative.")
    
    attachment = attachments[0]
    attachment_url = attachment.get('downloadUrl', '')
    attachment_title = attachment.get('title', 'No Title')

    if not attachment_url:
        raise HTTPException(status_code=404, detail="Attachment download URL not found.")
    
    try:
        # Download the PDF and extract text
        pdf_file_path = download_pdf_to_tempfile(attachment_url)
        extracted_text = extract_text_from_pdf(pdf_file_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to download or extract text from PDF: {e}")
    
    # Summarize the extracted text
    llm = ChatOpenAI(temperature=0.5, model_name="gpt-4o-mini", openai_api_key=api_key)
    summary_prompt = f"Please summarize the following text in less than 150 words: \n\n{extracted_text}\n\ntitle: {attachment_title}"
    
    # Generate summary with chain
    summary_chain = LLMChain(llm=llm, prompt=PromptTemplate(input_variables=["extracted_text", "attachment_title"], template=summary_prompt))
    summary_response = summary_chain.invoke({
        "extracted_text": extracted_text,
        "attachment_title": attachment_title
    })

    summary = summary_response.get('text', 'No summary generated.')
    
    return {
        "initiative_id": initiative_id,
        "attachment_title": attachment_title,
        "summary": summary
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
