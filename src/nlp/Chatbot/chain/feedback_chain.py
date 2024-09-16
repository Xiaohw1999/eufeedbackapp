# feedback_chain.py

import os
import dotenv
import pandas as pd
from pymongo import MongoClient
from fastapi import FastAPI, HTTPException, Request
from langchain_openai import OpenAIEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import RetrievalQA, ConversationalRetrievalChain
from langchain_openai import ChatOpenAI
from langchain_mongodb.vectorstores import MongoDBAtlasVectorSearch # test
from langchain.memory import ConversationBufferMemory 
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Query
from typing import List
import logging
import sys

# utf-8
sys.stdout.reconfigure(encoding='utf-8')

# Configure logging
logging.basicConfig(level=logging.INFO, encoding='utf-8')
logger = logging.getLogger(__name__)

# Load environment variables from the .env file
dotenv.load_dotenv()

# Initialize FastAPI app
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define parse_parameters function to create filter conditions
def parse_parameters(topic=None):
    """
    Parse the input parameters and construct search conditions for MongoDB.
    Args:
    - topic (str): The topic to filter by. If 'None', no filtering by topic is applied.
    Returns:
    - dict: Constructed search conditions to be used in MongoDB Atlas VectorSearch.
    """
    must_conditions = []

    # Add topic condition
    if topic:
        filter = {
            "text": {
                "path": "topic",
                "query": topic,
            }
        }
        must_conditions.append(filter)

    # Return the constructed conditions
    if must_conditions:
        return {
            "compound": {
                "must": must_conditions
            }
        }
    else:
        return {}

# Get MongoDB Atlas credentials from environment variables
ATLAS_TOKEN = os.environ["ATLAS_TOKEN"]
ATLAS_USER = os.environ["ATLAS_USER"]
# Initialize MongoDB Connection
client = MongoClient(
    "mongodb+srv://{}:{}@cluster0.9tj38oe.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0".format(
            ATLAS_USER, ATLAS_TOKEN)
)
db_name = "metadata"
collection_name = "processed_feedback_data"
collection_search_name = "keywords_search_data"
collection = client[db_name][collection_name]

# Check for the OpenAI API key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("Please set your API key in the OPENAI_API_KEY environment variable.")

# Set up embeddings, vectors, and memory for the retrieval chain
print("Setting up embeddings, vectors, and memory...")
embeddings = OpenAIEmbeddings(openai_api_key=api_key, 
                              model="text-embedding-3-small") # define embeddings to text-embedding-3-small

'''set up mmr method'''
# retriever = vectors.as_retriever(
#     search_type='mmr',
#     search_kwargs={'k': 5, 'lambda_mult': 0.1,}
#     )

# Initialize vector search with pre-filter
vectors = MongoDBAtlasVectorSearch(
    collection=collection, 
    index_name='metadata_vector_index',
    embedding=embeddings, 
    text_key='combined',
    embedding_key='embedding',
    relevance_score_fn="cosine",
)

prompt_template = """
    You are a helpful assistant responsible for providing detailed analysis and summaries of citizen feedback on EU laws and initiatives.

    ### Task:
    You have been given a question: {question}. The person asking this question could be a policymaker, researcher, or anyone interested in public feedback. They need you to provide in-depth analysis and summaries based on citizen feedback to help them understand public opinions and concerns.

    ### Context:
    The following contexts {context} have been provided to you, retrieved from a database of citizen feedback. Only use the information from the contexts provided to answer the question, and avoid speculation or using unprovided information. Due to the retrieval process, some contexts may be less relevant to the question; summarize these cautiously. If none of the contexts provide relevant information, politely express that you do not have enough information to answer the question.

    ### Context Structure:
    Each context provided to you includes the following information:
    - The type of user or organization: from context['UserType'] and context['Organization']
    - The country of the feedback provider: from context['Country']
    - A detailed and concrete summary of the feedback: from context['Content'] and context['Title']

    ### Requirements:
    Please summarize and analyze the content provided, paying attention to the following points:
    1. **Paragraph-based Summaries**: Avoid summarizing in a list format. Use paragraphs to separate different points when necessary.
    2. **Focus on Relevant Content**: Prioritize information that is directly related to the question. Briefly mention or skip content that is less relevant.
    3. **Polite Expression**: If you cannot provide a relevant answer, politely state "I'm not sure" or "Based on the provided context, I cannot answer this question."
    """
QA_CHAIN_PROMPT = ChatPromptTemplate.from_template(prompt_template)

# memory = ConversationBufferMemory( 
#     memory_key='chat_history', 
#     return_messages=True,
#     output_key='answer'
#     ) 

def create_conversational_chain(llm, retriever):
    conversational_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        # memory=memory,
        combine_docs_chain_kwargs={"prompt": QA_CHAIN_PROMPT},
        return_source_documents=True,
        output_key='answer'
    )
    
    return conversational_chain

def create_retrieval_qa_chain(llm, retriever):
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs={"prompt": QA_CHAIN_PROMPT},
    )
    
    return qa_chain

@app.post("/query")
async def get_feedback(request: Request):
    try:
        data = await request.json()
        query = data.get("query")
        topic = data.get("topic")
        chain_type = data.get("chain_type", "retrievalqa")
        model_name = data.get("model_name", "gpt-4o-mini")
        search_type = data.get("search_type", "similarity")
        search_kwargs = data.get("search_kwargs", {'k': 5})
        if not query:
            raise HTTPException(status_code=400, detail="Query parameter is required.")
        
        # Log the received query
        logger.info(f"Received query: {query}")
        
        # Generate pre-filter conditions using parse_parameters
        pre_filter_conditions = parse_parameters(topic=topic)
        search_kwargs['filter'] = pre_filter_conditions
        
        # Dynamically create the LLM based on model_name
        llm = ChatOpenAI(temperature=0.5, model_name=model_name, openai_api_key=api_key)
        
        # creat retriever and use combined search_kwargs
        retriever = vectors.as_retriever(
            search_type=search_type,
            search_kwargs=search_kwargs
        )
        
        # Select the appropriate chain based on the request
        if chain_type == "conversational":
            chain = create_conversational_chain(llm, retriever)
            response = chain.invoke({"question": query, "chat_history": []})
            answer = response.get('answer', 'No answer found')
        elif chain_type == "retrievalqa":
            chain = create_retrieval_qa_chain(llm, retriever)
            response = chain.invoke({"query": query})
            answer = response.get('result', 'No answer found')
        
        # Log the raw response for debugging  
        logger.info(f"Response: {response}")

        source_documents = response.get('source_documents', [])
        sources = [{"text": doc.page_content} for doc in source_documents]
        print(sources[0])
        return {"response": answer, "sources": sources}

    except Exception as e:
        logger.error(f"Error processing request: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

# api for keywords search
collection_search = client[db_name][collection_search_name]

@app.get("/search_keywords", response_model=List[dict])
async def search_keywords(keyword: str = Query(..., min_length=1)):
    if not keyword or keyword.strip() == "":
        raise HTTPException(status_code=400, detail="Keyword parameter is required.")
    
    search_conditions = [
        {"shortTitle": {"$regex": keyword, "$options": "i"}},
        {"id": {"$regex": keyword, "$options": "i"}}
    ]
    results = list(collection_search.find(
        {
            "$or": search_conditions
        },
        {"_id": 0, "id": 1, "shortTitle": 1, "topic": 1, "totalFeedback": 1, "links": 1}
    ))
    
    if not results:
        raise HTTPException(status_code=404, detail="No matching documents found.")
    
    return results

# solely for test & debug
@app.get("/test")
def test_endpoint():
    print("Test endpoint called!")
    return {"message": "Test successful"}

# Run the FastAPI app using uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
    
    # uvicorn feedback_chain:app --reload
    
# scp -i "D:\aws_key\aws_node.pem" "D:\visualstudiocode\project\eufeedbackapp\src\nlp\Chatbot\chain\feedback_chain.py" ec2-user@ec2-16-171-132-28.eu-north-1.compute.amazonaws.com:/home/ec2-user/eufeedbackapp
# sudo systemctl restart my-fastapi-app.service
# sudo nano /etc/systemd/system/my-fastapi-app.service
# sudo systemctl status my-fastapi-app