import json
import requests

def fetch_all_data_from_api(api_url, limit=100):
    api_data = []
    while api_url:
        response = requests.get(api_url, params={'limit': limit})
        if response.status_code == 200:
            data = response.json()
            results = data.get("results", [])
            api_data.extend(results)
            api_url = data.get("next")
        else:
            raise Exception(f"Error: {response.status_code}")
        
    with open('api_data.json', 'w') as json_file:
        json.dump(api_data, json_file)
                
    return api_data
