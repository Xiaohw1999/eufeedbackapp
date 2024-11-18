import pandas as pd
import json
import os

# 定义文件路径
topic = 'AGRI'
SRC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
input_file_path = os.path.join(SRC_DIR, 'data', topic, 'embedded_data.csv')
output_file_path = os.path.join(SRC_DIR, 'data', topic, 'embedded_data.csv')

# 读取数据
df = pd.read_csv(input_file_path)

# 将嵌入向量从字符串格式转换回列表格式
df['embedding'] = df['embedding'].apply(json.loads)

# 保存到新的CSV文件
df.to_csv(output_file_path, index=False)

print("Embedding correction and saving to local file completed.")
