import os 
import sys
import pandas as pd

# root path
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
print("Base Dir:", BASE_DIR)
SRC_DIR = os.path.join(BASE_DIR, 'src')

# add root to sys.path
sys.path.append(BASE_DIR)

# project path
DATA_DIR = os.path.join(SRC_DIR, 'data')
print("Data Dir:", DATA_DIR)
# file = pd.read_csv(os.path.join(DATA_DIR, 'AGRI/embedding_data.csv'))
# print(file.head())
ML_DIR = os.path.join(SRC_DIR, 'machine_learning')
print("ML Dir:", ML_DIR)
SCRAPING_DIR = os.path.join(SRC_DIR, 'scraping')
print("Scraping Dir:", SCRAPING_DIR)
DB_DIR = os.path.join(SRC_DIR, 'database')
print("DB Dir:", DB_DIR)
FROTEND_DIR = os.path.join(SRC_DIR, 'frontend')
print("Frontend Dir:", FROTEND_DIR)

__all__ = [
    'BASE_DIR',
    'SRC_DIR',
    'DATA_DIR',
    'ML_DIR',
    'SCRAPING_DIR',
    'DB_DIR',
    'FROTEND_DIR']