import os
import pymongo
from pymongo import UpdateOne

database_metadata = 'metadata'
metadata_collection_name = 'feedbackinfo_data'
processeddata_collection_name = 'processed_feedback_data'
progress_collection_name = 'processing_progress'

keywords_collection_name = 'keywords_search_data'

username = os.getenv('ATLAS_USER')
password = os.getenv('ATLAS_TOKEN')
if not username or not password:
    raise ValueError("Missing MongoDB credentials")

uri = f"mongodb+srv://{username}:{password}@cluster0.9tj38oe.mongodb.net/{database_metadata}?retryWrites=true&w=majority"
client = pymongo.MongoClient(uri)

def create_and_update_keywords_collection():
    db = client[database_metadata]
    feedbackinfo_collection = db[metadata_collection_name]
    keywords_search_collection = db[keywords_collection_name]
    
    feedbackinfo_data = feedbackinfo_collection.find({}, {"_id": 1, "id": 1, "shortTitle": 1, "topic": 1, "totalFeedback": 1})

    operations = []
    seen_ids = set()
    
    for document in feedbackinfo_data:
        document_id_str = str(document["id"])
        
        if document_id_str in seen_ids:
            continue  # Skip if we've already processed this ID
        
        seen_ids.add(document_id_str)
        
        link = f"https://ec.europa.eu/info/law/better-regulation/have-your-say/initiatives/{document['id']}"
        
        # transfer id to string
        # document_id_str = str(document["id"])
        document_totalFeedback_str = str(document["totalFeedback"])
        
        # Update
        operations.append(
            UpdateOne(
                {"_id": document["_id"]},
                {
                    "$set": {
                        "id": document_id_str, 
                        "shortTitle": document["shortTitle"],
                        "topic": document["topic"],
                        "totalFeedback": document_totalFeedback_str,
                        "links": link
                    }
                },
                upsert=True
            )
        )
    if operations:
        result = keywords_search_collection.bulk_write(operations)
        print(f"Matched: {result.matched_count}, Modified: {result.modified_count}, Upserted: {result.upserted_count}")


def main():
    create_and_update_keywords_collection()
    
if __name__ == "__main__":
    main()