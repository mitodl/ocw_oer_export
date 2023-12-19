import requests
import logging
from retry import retry
from data_loader import save_data_to_json

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

@retry(tries=3, delay=2, logger=logger)
def fetch_all_data_from_api(api_url, limit=100, output_file='api_data.json'):
    api_data = []
    local_count = 0  # Local count of objects accumulated

    try:
        while api_url:
            response = requests.get(api_url, params={'limit': limit})
            response.raise_for_status()
            data = response.json()
            results = data.get("results", [])
            api_data.extend(results)
            api_url = data.get("next")
            
            # Update the local count
            local_count += len(results)

            # Calculate the progress percentage
            progress_percentage = (local_count / data.get("count", 1)) * 100
            logger.info(f"% API loaded - Progress: {progress_percentage:.2f}%\r")

    except requests.RequestException as e:
        logger.error(f"Error fetching data from API: {e}")
    else:
        save_data_to_json(api_data, output_file)

    return api_data
