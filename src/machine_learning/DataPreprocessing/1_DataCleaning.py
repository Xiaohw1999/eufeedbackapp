# final version of data: Id, shorttitle, country, language, feedback
import os
import json
import pandas as pd

def load_data(file_path, file_name):
    full_path = os.path.join(file_path, file_name)
    if not os.path.exists(full_path):
        print(f"File '{file_name}' does not exist.")
        return None   
    with open(full_path, 'r', encoding='utf-8') as file:
        return json.load(file)
    
def filter_feedback(data):
    return [item for item in data if item.get("feedback") != "no data"]

# merge data from 'initiatives_id.json' and 'feedback_info.json'
def merge_data(initiatives, feedbacks):
    
    # merge feedbacks with the same initiative id
    feedback_dict = {}
    for item in feedbacks:
        id = item['id']
        if id in feedback_dict:
            feedback_dict[id].append(item)
        else:
            feedback_dict[id] = [item]
            
    # merge initiatives and feedbacks 
    merged_data = []
    for initiative in initiatives:
        feedback_items = feedback_dict.get(initiative["id"], [])
        for feedback_item in feedback_items:
            for feedback in feedback_item["feedback"]["_embedded"]["feedback"]:
                merged_item = {
                    "id": initiative["id"],
                    "short_title": initiative["short_title"],
                    "Feedback": feedback.get("feedback"),
                    "Feedback_id": feedback.get("id"),
                    "country": feedback.get("country"),
                    "language": feedback.get("language")
                }
                merged_data.append(merged_item)
    return merged_data
    
def data_preprocessing(data):

    df = pd.DataFrame(data)
    # delete feedback = null
    df = df[df['Feedback'].notnull()]
    # lower, remove /n
    if 'Feedback' in df.columns:
        df['Feedback'] = df['Feedback'].apply(lambda x: " ".join(x.split()).lower())
    # delete same data
    df.drop_duplicates(inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df

if __name__ == '__main__':
    topic = 'AGRI'
    SRC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    data_dir = os.path.join(SRC_DIR, 'data', topic)
    
    # Load data
    initiatives = load_data(data_dir, 'initiatives_id.json')
    feedback_info = load_data(data_dir, 'feedback_info.json')

    # Filter and merge data
    filtered_feedback = filter_feedback(feedback_info)
    merged_data = merge_data(initiatives, filtered_feedback)

    # Preprocess data
    final_df = data_preprocessing(merged_data)
    print(final_df.head())

    # Save processed data to a new file
    output_path = os.path.join(data_dir, 'processed_data.csv')
    final_df.to_csv(output_path, index=False)