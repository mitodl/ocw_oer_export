import json
import pandas as pd
from dotenv import load_dotenv
from os import getenv

from client import fetch_all_data_from_api
load_dotenv()

def load_api_data_from_json(filename='api_data.json'):
    try:
        with open(filename, 'r') as json_file:
            all_data = json.load(json_file)
        print("Data successfully loaded from JSON file.")
        return all_data
    except FileNotFoundError:
        print(f"{filename} not found.")
        return []

def ocw_topic_to_oer_subject_mapping(filename='mapping_files/ocw_topic_to_oer_subject.csv'):
    ocw_topic_to_subject = pd.read_csv(filename)
    topic_mapping = ocw_topic_to_subject['OER Subject'].to_dict()
    missing_subjects = ocw_topic_to_subject[ocw_topic_to_subject['OER Subject'].isna()]
    topic_mapping.update(missing_subjects.set_index('OCW Topic')['OER Keyword'].to_dict())
    return topic_mapping

def process_data(data):
    processed_data = [{"CR_TITLE": result["title"], "CR_URL": result["runs"][0]["url"], "CR_LANGUAGE": "en", "CR_COU_TITLE": "Creative Commons Attribution Non Commercial Share Alike 4.0", "CR_PRIMARY_USER": "student|teacher"} for result in data if result.get("runs")]
    return processed_data

def main():
    api_url = getenv('API_URL')
    api_data_json = load_api_data_from_json()

    processed_data = process_data(api_data_json)

    final_df = pd.DataFrame(processed_data, columns=["CR_TITLE", "CR_URL", "CR_LANGUAGE", "CR_COU_TITLE", "CR_PRIMARY_USER"])

    # print(final_df)
    ocw_topic_to_oer_subject_mapping()

    final_df.to_csv('transformed_data.csv', index=False)

if __name__ == "__main__":
    main()
