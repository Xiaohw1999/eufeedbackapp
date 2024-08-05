import os
import dotenv
import pandas as pd
from pymongo import MongoClient
from fastapi import FastAPI, HTTPException, Request
from langchain_openai import OpenAIEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain.chains import RetrievalQA, ConversationalRetrievalChain
from langchain_openai import ChatOpenAI
from langchain_mongodb import MongoDBAtlasVectorSearch # test
from langchain.memory import ConversationBufferMemory 
from fastapi.middleware.cors import CORSMiddleware
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
collection = client[db_name][collection_name]

# Check for the OpenAI API key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("Please set your API key in the OPENAI_API_KEY environment variable.")

# Set up embeddings, vectors, and memory for the retrieval chain
print("Setting up embeddings, vectors, and memory...")
embeddings = OpenAIEmbeddings(openai_api_key=api_key, 
                              model="text-embedding-3-small") # define embeddings to text-embedding-3-small
vectors = MongoDBAtlasVectorSearch(
    collection=collection, 
    index_name='metadata_vector_index',
    embedding=embeddings, 
    text_key='combined',
    embedding_key='embedding'
    )

'''set up mmr method'''
# retriever = vectors.as_retriever(
#     search_type='mmr',
#     search_kwargs={'k': 5, 'lambda_mult': 0.1,}
#     )

'''set up similarity method'''
retriever = vectors.as_retriever(
    search_type='similarity',
    search_kwargs={'k': 5}
    )

memory = ConversationBufferMemory( 
    memory_key='chat_history', 
    return_messages=True, 
    output_key='answer'
    ) 

llm = ChatOpenAI(temperature=0.5, model_name='gpt-3.5-turbo', openai_api_key=api_key)

prompt_template = """You are a helpful assistant providing detailed analysis and summaries of citizen feedback on EU laws and initiatives. Some feedback may not be in English, so use your translation skills to understand them. Please answer in a friendly and natural manner, just like a normal conversation. If you don't know an answer, say you don't know.

Using the information from the context given to you, but do not make up information that is not in the context, provide your answer as detailed and concise as possible.
For all feedbacks in the given context which is relevant to the given question, answer with the below information in a natural way.

- The type of user or organization: from context['UserType']
- The country of the feedback provider: from context['Country']
- A detailed and concrete summary of the feedback: from context['Content'] and context['Title']
- An analysis of all feedback, including any common themes or notable points

Contexts:
{context}
Question: {question}
"""
QA_CHAIN_PROMPT = PromptTemplate(
    input_variables=["context", "question"],
    template=prompt_template,
    )

'''set up the retrieval chain with ConversationalRetrievalChain'''
# chain = ConversationalRetrievalChain.from_llm(
#     llm=llm, 
#     retriever=retriever,
#     # memory = memory,
#     return_source_documents=True,
#     combine_docs_chain_kwargs={"prompt": QA_CHAIN_PROMPT},
#     output_key='answer'
#     )

'''set up the retrieval chain with RetrievalQA'''
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever,
    return_source_documents=True,
    chain_type_kwargs={"prompt": QA_CHAIN_PROMPT},
)

@app.post("/query")
async def get_feedback(request: Request):
    try:
        data = await request.json()
        query = data.get("query")
        if not query:
            raise HTTPException(status_code=400, detail="Query parameter is required.")
        
        # Log the received query
        logger.info(f"Received query: {query}")
        
        # Get the results from the output
        
        '''get response use ConversationalRetrievalChain'''
        # response = chain.invoke({"question": query, "chat_history": []})
        # answer = response.get('answer', 'No answer found')
        
        '''get response use qa chain'''
        response = qa_chain.invoke({"query": query})
        answer = response.get('result', 'No answer found')
        
        # Log the raw response for debugging
        # logger.info(f"Raw response: {response}")

        source_documents = response.get('source_documents', [])
        sources = [{"text": doc.page_content} for doc in source_documents]
        print(sources[0])
        return {"response": answer, "sources": sources}

    except Exception as e:
        logger.error(f"Error processing request: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

#solely for test & debug
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
    