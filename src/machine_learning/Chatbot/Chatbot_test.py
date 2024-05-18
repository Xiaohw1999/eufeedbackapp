import pandas as pd

df = pd.read_csv('D:/visualstudiocode/project/Eu_Feedback/scraping/PythonScraping/EU_Commision/data/AGRI/embedding_data.csv', index_col=0)
if 'Unnamed: 0' in df.columns:
    df.drop(columns='Unnamed: 0', inplace=True)
df.to_csv('D:/visualstudiocode/project/Eu_Feedback/scraping/PythonScraping/EU_Commision/data/AGRI/embedding_data.csv', index=False)