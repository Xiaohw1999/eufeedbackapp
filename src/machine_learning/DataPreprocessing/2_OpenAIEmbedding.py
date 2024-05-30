import os
import pandas
from dotenv import load_dotenv
load_dotenv()
import time
from openai import OpenAI
from concurrent.futures import ThreadPoolExecutor

def generate_embeddings(text):
    '''
    Generate embeddings from string of text.
    This will be used to vectorize data and user input for interactions with Azure OpenAI.
    '''
    text = text.replace("\n", " ")
    response = client.embeddings.create(input=[text], model='text-embedding-3-small') 
    print('Done')
    return response.data[0].embedding

if __name__ == "__main__":
    # generate embeddings for all text in the dataframe
    api_key = os.environ["OPENAI_API_KEY"]
    client = OpenAI(api_key=api_key)

    # load csv
    topic = 'AGRI'
    SRC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    processed_file_path = os.path.join(SRC_DIR, 'data', topic, 'processed_data.csv')
    df = pandas.read_csv(processed_file_path)
    df['embedding'] = df['Feedback'].apply(generate_embeddings)
    embedding_file_path = os.path.join(SRC_DIR, 'data', topic, 'embedding_data.csv')
    df.to_csv(embedding_file_path, index=False)
