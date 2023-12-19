import requests
from data_loader import save_data_to_json

def fetch_all_data_from_api(api_url, limit=100, output_file='api_data.json'):
    api_data = []
    while api_url:
        try:
            response = requests.get(api_url, params={'limit': limit})
            response.raise_for_status()
            data = response.json()
            results = data.get("results", [])
            api_data.extend(results)
            api_url = data.get("next")
        except requests.RequestException as e:
            print(f"Error fetching data from API: {e}")

    save_data_to_json(api_data, output_file)

    return api_data
