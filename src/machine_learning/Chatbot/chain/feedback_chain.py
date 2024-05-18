import os
import dotenv
import pandas as pd
from pymongo import MongoClient
from fastapi import FastAPI, HTTPException, Request
from langchain_openai import OpenAIEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI
from langchain_mongodb import MongoDBAtlasVectorSearch # test
from langchain.memory import ConversationBufferMemory 
from langchain.chains import ConversationalRetrievalChain


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
embeddings = OpenAIEmbeddings(openai_api_key=api_key)
vectors = MongoDBAtlasVectorSearch.from_connection_string(
    "mongodb+srv://{}:{}@cluster0.9tj38oe.mongodb.net/".format(
            ATLAS_USER, ATLAS_TOKEN),
    f"{db_name}.{collection_name}",
    # collection=collection, 
    index_name='embedded_index',
    embedding=embeddings, 
    text_key='Feedback',
    embedding_key='Embedding'
    )
retriever = vectors.as_retriever(
    # search_type='similarity',
    # search_kwargs={'k': 15}
    # search_type='mmr',
    # search_kwargs={'k': 5, 'lambda_mult': 0.25,}
    )

memory = ConversationBufferMemory( 
    memory_key='chat_history', 
    return_messages=True, 
    ) 

llm = ChatOpenAI(temperature=0.5, model_name='gpt-3.5-turbo', openai_api_key=api_key)

prompt_template = """Use these feedback context from citizens to answer and summarize questions about EU laws and initiatives and citizens' opinions. 
Please be as specific as possible, but don't make up any information that's not from the context. 
If you don't know an answer, say you don't know. Also you are a friendly chatbot who is always polite.
{context}
Question: {question}
"""
QA_CHAIN_PROMPT = PromptTemplate(
    input_variables=["context", "question"],
    template=prompt_template,
    )

#set up the retrieval chain

chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    chain_type='stuff',
    memory=memory,
    chain_type_kwargs={
        "prompt": QA_CHAIN_PROMPT,
        # "memory": memory
        }
    )

# chain = ConversationalRetrievalChain.from_llm(
#     llm=llm, 
#     retriever=vectors.as_retriever(search_type = 'mmr',
#                                     search_kwargs={
#                                             'k': 100, 'lambda_mult': 0.25,
#                                     }),
#     memory = memory,
#     return_source_documents=True,
#     return_generated_question=True,
#     combine_docs_chain_kwargs={"prompt": QA_CHAIN_PROMPT}
#     )


@app.post("/query")
async def get_feedback(request: Request):
    try:
        data = await request.json()
        query = data.get("query")
        if not query:
            raise HTTPException(status_code=400, detail="Query parameter is required.")
        # get the results from the output
        response = chain.invoke(input={'query': query})['result']
        # print(memory.buffer)
        return {"response": response}

    except Exception as e:
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