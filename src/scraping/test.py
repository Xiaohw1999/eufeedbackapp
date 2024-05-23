import requests
import json
import os
import time

url_initiatives_id = 'https://ec.europa.eu/info/law/better-regulation/brpapi/searchInitiatives?'

def get_init_id(url, topic, size, language):
    page = 0
    info = []
    

    params = {
        'topic': topic,
        'size': size,
        'page': page,
        'language': language,
        
    }
    response = requests.get(url, params=params)
    data = response.json()
    # initiatives_data = data.get('_embedded', {}).get('initiativesResultDtoes', [])
    # for item in initiatives_data:
    #     id = int(item.get('id'))
    #     status = item.get('initiativeStatus')
    #     short_title = item.get('shortTitle')
    #     info.append({'id': id, 'status': status, 'short_title': short_title})
    #     print(f'{id} success')
    
    print (data.get("_embedded", {}).get("initiativeResultDtoes", []))

get_init_id(url_initiatives_id, 'AGRI', 10, 'EN')