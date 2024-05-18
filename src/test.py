import pandas as pd


path = 'src/data/AGRI/embedding_data.csv'
dataframe = pd.read_csv(path)
print(dataframe.head())