"""
Module for loading and saving data to/from JSON files.
"""
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_data_from_json(filename):
    """Load data from a JSON file."""
    try:
        with open(filename, "r", encoding="utf-8") as json_file:
            data = json.load(json_file)
            logger.info("Data successfully loaded from %s.", filename)
            return data
    except FileNotFoundError:
        logger.error("%s not found.", filename)
        return []


def save_data_to_json(data, filename):
    """Save data to a JSON file."""
    with open(filename, "r", encoding="utf-8") as json_file:
        json.dump(data, json_file)
        logger.info("Data successfully saved to %s.", filename)
