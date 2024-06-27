import os
import json
import asyncio
import time
from ScrapingPiplineWithPDF import get_init_id, get_publication_id, get_feedback_info, convert_objectid_to_str
from aiohttp_retry import RetryClient, ExponentialRetry

async def main():
    topic_list = ['AGRI']
    total_feedback = []
    for topic in topic_list:
        start_time = time.time()
        page = 0

        semaphore = asyncio.Semaphore(10)
        retry_options = ExponentialRetry(attempts=5)
        
        async with RetryClient(raise_for_status=False, retry_options=retry_options) as session:
            while True:
                print(f'Processing page {page} for topic {topic}')
                id_list, total_pages = await get_init_id(session, topic, size=10, language='en', page=page, semaphore=semaphore)
                if not id_list:
                    break
                pubid = await get_publication_id(session, id_list, semaphore)
                feedback_info = await get_feedback_info(session, pubid, topic, semaphore)
                # Convert ObjectId to string before saving to JSON
                feedback_info_str = convert_objectid_to_str(feedback_info)
                if page >= total_pages - 1:
                    break
                page += 1
        
                total_feedback.extend(feedback_info_str)
        output = 'D:/visualstudiocode/project/eufeedbackapp/src/database/test_data'
        final_file = os.path.join(output, f'test_data.json')
        if not os.path.exists(output):
            os.makedirs(output)
        
        with open(final_file, 'w', encoding='utf-8') as f:
            json.dump(total_feedback, f, ensure_ascii=False, indent=4)
        
        end_time = time.time()
        print(f'Total processing time for topic {topic}: {end_time - start_time} seconds')

if __name__ == '__main__':
    asyncio.run(main())