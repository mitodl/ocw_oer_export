"""
Module for extracting and loading data to/from JSON file
"""
import json
import logging


def extract_data_from_json(filename):
    """Extract data from a JSON file."""
    try:
        with open(filename, "r", encoding="utf-8") as json_file:
            data = json.load(json_file)
            logging.info("Data successfully extracted from %s.", filename)
            return data
    except FileNotFoundError as exc:
        raise FileNotFoundError(f"{filename} not found.") from exc


def load_data_to_json(data, filename):
    """Save data to a JSON file."""
    with open(filename, "r", encoding="utf-8") as json_file:
        json.dump(data, json_file)
        logging.info("Data successfully saved to %s.", filename)
