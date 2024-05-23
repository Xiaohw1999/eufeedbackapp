import os
from dotenv import load_dotenv

# 获取项目根目录路径
SRC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
file_path = os.path.join(SRC_DIR, 'data', 'AGRI', 'initiatives_id.json')
print(file_path)