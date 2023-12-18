import json
import pandas as pd
from dotenv import load_dotenv
from os import getenv

from client import fetch_all_data_from_api
from utilities.markdown_to_text import unmark
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

def create_ocw_topic_to_oer_subject_mapping(filename='mapping_files/ocw_topic_to_oer_subject.csv'):
    ocw_topic_to_subject = pd.read_csv(filename)
    ocw_topics_mapping = ocw_topic_to_subject.set_index('OCW Topic')['OER Subject'].to_dict()
    return ocw_topics_mapping

def get_cr_subjects(ocw_topics_mapping, ocw_course_topics):
    # Returns pipe-separated string of OER subjects for an OCW course
    oer_subjects_list = [ocw_topics_mapping.get(topic['name']).split('|') if ocw_topics_mapping.get(topic['name']) is not None else [] for topic in ocw_course_topics]
    unique_oer_subjects = set(subject for subjects in oer_subjects_list for subject in subjects)
    return '|'.join(unique_oer_subjects)

def get_cr_keywords(list_of_topics_objs):
    # Returns pipe-separated string of keywords from OCW topics
    return'|'.join(topic['name'] for topic in list_of_topics_objs)

def get_cr_authors(list_of_authors_objs):
    # Returns pipe-separated string of keywords from Authors
    return'|'.join(f"{author['last_name']}, {author['first_name']}" for author in list_of_authors_objs)

def get_cr_educational_use(resource_content_tags):
    # Returns pipe-separated string of educational uses from Resource Content Tags
    tags = ["Curriculum/Instruction"]
    assessment_flag = any("Assignment" in tag for tag in resource_content_tags)
    professional_dev_flag = "Instructor Insights" in resource_content_tags
    
    if assessment_flag:
        tags.append("Assessment")
    
    if professional_dev_flag:
        tags.append("Professional Development")
    
    return "|".join(tags)

def get_cr_accessibility(resource_content_tags):
    # Returns pipe-separated string of accessibility uses from Resource Content Tags
    tags = ["Visual|Textual"]
    video_flag = any("Video" in tag for tag in resource_content_tags)
    
    if video_flag:
        tags.append("Auditory|Caption|Transcript")
    
    return "|".join(tags) 


def get_description_in_plain_text(description):
    stripped_markdown = unmark(description)
    return unmark(description)


def process_data(data):
    ocw_topics_mapping = create_ocw_topic_to_oer_subject_mapping()

    processed_data = [{"CR_TITLE": result["title"], "CR_URL": result["runs"][0]["url"], "CR_MATERIAL_TYPE": "Full Course", "CR_Media_Formats": "Text/HTML", "CR_ABSTRACT": get_description_in_plain_text(result["runs"][0]["description"]), "CR_LANGUAGE": "en", "CR_COU_TITLE": "Creative Commons Attribution Non Commercial Share Alike 4.0", "CR_PRIMARY_USER": "student|teacher", "CR_SUBJECT": get_cr_subjects(ocw_topics_mapping, result["topics"]), "CR_KEYWORDS": get_cr_keywords(result["topics"]), "CR_AUTHOR_NAME": get_cr_authors(result["runs"][0]["instructors"]), "CR_PROVIDER": "MIT", "CR_PROVIDER_SET": "MIT OpenCourseWare", "CR_COU_URL": "https://creativecommons.org/licenses/by-nc-sa/4.0/", "CR_COU_COPYRIGHT_HOLDER": "MIT", "CR_EDUCATIONAL_USE": get_cr_educational_use(result["resource_content_tags"]), "CR_ACCESSIBILITY": get_cr_accessibility(result["resource_content_tags"])} for result in data if result.get("runs")]
    return processed_data

def main():
    api_url = getenv('API_URL')
    api_data_json = load_api_data_from_json()
    processed_data = process_data(api_data_json)
    final_df = pd.DataFrame(processed_data, columns=["CR_TITLE", "CR_URL", "CR_MATERIAL_TYPE", "CR_Media_Formats", "CR_ABSTRACT", "CR_LANGUAGE", "CR_COU_TITLE", "CR_PRIMARY_USER", "CR_SUBJECT", "CR_KEYWORDS", "CR_AUTHOR_NAME", "CR_PROVIDER", "CR_PROVIDER_SET", "CR_COU_URL", "CR_COU_COPYRIGHT_HOLDER", "CR_EDUCATIONAL_USE", "CR_ACCESSIBILITY"])

    print(final_df)

    final_df.to_csv('transformed_data.csv', index=False)

if __name__ == "__main__":
    main()
