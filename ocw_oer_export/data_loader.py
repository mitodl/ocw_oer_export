import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_data_from_json(filename):
    try:
        with open(filename, 'r') as json_file:
            data = json.load(json_file)
            logger.info(f"Data successfully loaded from {filename}.")
            return data
    except FileNotFoundError:
        logger.error(f"{filename} not found.")
        return []

def save_data_to_json(data, filename):
    with open(filename, 'w') as json_file:
        json.dump(data, json_file)
        logger.info(f"Data successfully saved to {filename}.")