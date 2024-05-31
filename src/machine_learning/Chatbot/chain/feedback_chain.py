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
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from the .env file
dotenv.load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Get MongoDB Atlas credentials from environment variables
ATLAS_TOKEN = os.environ["ATLAS_TOKEN"]
ATLAS_USER = os.environ["ATLAS_USER"]
# Initialize MongoDB Connection
client = MongoClient(
    "mongodb+srv://{}:{}@cluster0.9tj38oe.mongodb.net/".format(
            ATLAS_USER, ATLAS_TOKEN)
)
db_name = "citizen_feedback"
collection_name = "embedded_data"
collection = client[db_name][collection_name]

# Check for the OpenAI API key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("Please set your API key in the OPENAI_API_KEY environment variable.")

# Set up embeddings, vectors, and memory for the retrieval chain
print("Setting up embeddings, vectors, and memory...")
embeddings = OpenAIEmbeddings(openai_api_key=api_key, 
                              model="text-embedding-ada-002") # define embeddings to text-embedding-3-small
vectors = MongoDBAtlasVectorSearch(
    collection=collection, 
    index_name='embedded_index',
    embedding=embeddings, 
    text_key='Feedback',
    embedding_key='Embedding'
    )
retriever = vectors.as_retriever(
    # search_type='similarity',
    # search_kwargs={'k': 10}
    search_type='mmr',
    search_kwargs={'k': 15, 'lambda_mult': 0.6,}
    )

memory = ConversationBufferMemory( 
    memory_key='chat_history', 
    return_messages=True, 
    output_key='answer'
    ) 

llm = ChatOpenAI(temperature=0.5, model_name='gpt-3.5-turbo', openai_api_key=api_key)

prompt_template = """Use information in these contexts to answer questions. 
Each context is a paragraph of feedback from a citizen about a specific EU law or initiative topic.
Some of them are not write in english, use your powerful translation skill to understand them. 
Please answer as detailed as possible, but do not make up information that does not belong in the context.
If you don't know an answer, say you don't know. Also you are a friendly chatbot who is always polite.
Contexts:{context}
Question: {question}
"""
QA_CHAIN_PROMPT = PromptTemplate(
    input_variables=["context", "question"],
    template=prompt_template,
    )

#set up the retrieval chain
# chain = RetrievalQA.from_chain_type(
#     llm=llm,
#     retriever=retriever,
#     chain_type='stuff',
#     memory=memory,
#     chain_type_kwargs={
#         "prompt": QA_CHAIN_PROMPT,
#         # "memory": memory
#         }
#     )

chain = ConversationalRetrievalChain.from_llm(
    llm=llm, 
    retriever=retriever,
    memory = memory,
    return_source_documents=True,
    combine_docs_chain_kwargs={"prompt": QA_CHAIN_PROMPT},
    output_key='answer'
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
        
        # get the results from the output
        # response = chain.run({"question": query})
        # response = chain.invoke(input={'query': query})['result']
        # print(memory.buffer)
        response = chain.invoke({"question": query})
        
        # Log the raw response for debugging
        # logger.info(f"Raw response: {response}")

        answer = response.get('answer', 'No answer found')
        source_documents = response.get('source_documents', [])
        sources = [{"text": doc.page_content} for doc in source_documents]
        
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
    uvicorn.run(app, host="0.0.0.0", port=8000)
    
    # uvicorn feedback_chain:app --reload