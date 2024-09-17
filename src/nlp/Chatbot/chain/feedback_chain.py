# feedback_chain.py

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
                "query": topic
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
# client = MongoClient(
#     "mongodb+srv://{}:{}@cluster0.9tj38oe.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0".format(
#             ATLAS_USER, ATLAS_TOKEN)
# )

uri = f"mongodb+srv://{ATLAS_USER}:{ATLAS_TOKEN}@cluster0.nn50y.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri)

# uri = 'mongodb://localhost:27017/'
# client = MongoClient(uri)
db_name = "citizen_feedback"
collection_name = "AGRI_embedded_data"
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

'''set up similarity method'''

memory = ConversationBufferMemory( 
    memory_key='chat_history', 
    return_messages=True, 
    output_key='answer'
    ) 

llm = ChatOpenAI(temperature=0.5, model_name='gpt-3.5-turbo', openai_api_key=api_key)

prompt_template = """You are a helpful assistant providing detailed analysis and summaries of citizen feedback on EU laws and initiatives. 
Some feedback may not be in English, so use your translation skills to understand them. Please answer in a friendly and natural manner, just like a normal conversation. If you don't know an answer, say you don't know.

Using the information from the context given to you, but do not make up information that is not in the context, provide your answer as detailed and concise as possible, then answer with the below information in a natural way.

- The type of user or organization: from context['UserType'] and context['Organization']
- The country of the feedback provider: from context['Country']
- A detailed and concrete summary of the feedback: from context['Content'] and context['Title']
- An analysis of all feedback, including any common themes or notable points

Be careful not to summarize like a list, you can summarize in sections when facing different points. 
Your answer must be relevant to or from the question and context given to you.

Contexts:
{context}
Question: {question}
"""
QA_CHAIN_PROMPT = PromptTemplate(
    input_variables=["context", "question"],
    template=prompt_template,
    )

@app.post("/query")
async def get_feedback(request: Request):
    try:
        data = await request.json()
        query = data.get("query")
        topic = data.get("topic")
        if not query:
            raise HTTPException(status_code=400, detail="Query parameter is required.")
        
        # Log the received query
        logger.info(f"Received query: {query}")
        
        # Generate pre-filter conditions using parse_parameters
        pre_filter_conditions = parse_parameters(topic=topic)
        
        # Initialize vector search with pre-filter
        vectors = MongoDBAtlasVectorSearch(
            collection=collection, 
            index_name='metadata_vector_index',
            embedding=embeddings, 
            text_key='combined',
            embedding_key='embedding'
        )
        
        # Set up the retriever with pre-filter
        retriever = vectors.as_retriever(
            search_type='similarity',
            filter=pre_filter_conditions,
            search_kwargs={
                'k': 5,  # Retrieve the top 5 most relevant documents
            }
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
        
        '''Reinitialize the QA chain with the updated retriever'''
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True,
            chain_type_kwargs={"prompt": QA_CHAIN_PROMPT},
        )
        
        
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
        # print(sources[0])
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
