import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from .constants import API_URL
from .client import fetch_all_data_from_api

def create_json(output_file="ocw_api_data.json"):
    api_data = fetch_all_data_from_api(api_url=API_URL)
    try:
        with open(output_file, 'w', encoding='utf-8') as json_file:
            json.dump(api_data, json_file, ensure_ascii=False, indent=4)
        logger.info(f"Data saved to {output_file} at present directory.")
    except IOError as e:
        logger.error(f"Error saving data to JSON: {e}")