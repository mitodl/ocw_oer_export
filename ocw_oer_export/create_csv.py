import os.path
import pandas as pd
import logging

from .client import fetch_all_data_from_api
from .data_loader import load_data_from_json
from .constants import API_URL
from .utilities import cleanup_curly_brackets, html_to_text, markdown_to_text

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_ocw_topic_to_oer_subject_mapping(path=None, file_name=None):
    if path is None:
        path = os.path.dirname(__file__)

    if file_name is None:
        file_name = 'mapping_files/ocw_topic_to_oer_subject.csv'

    file_path = os.path.join(path, file_name)
    ocw_topic_to_subject = pd.read_csv(file_path)
    ocw_topics_mapping = ocw_topic_to_subject.set_index('OCW Topic')['OER Subject'].to_dict()
    return ocw_topics_mapping

def get_cr_subjects(ocw_topics_mapping, ocw_course_topics):
    oer_subjects_list = [ocw_topics_mapping.get(topic['name']).split('|') if ocw_topics_mapping.get(
        topic['name']) is not None else [] for topic in ocw_course_topics]
    unique_oer_subjects = set(subject for subjects in oer_subjects_list for subject in subjects)
    return '|'.join(unique_oer_subjects)

def get_cr_keywords(list_of_topics_objs):
    return '|'.join(topic['name'] for topic in list_of_topics_objs)

def get_cr_authors(list_of_authors_objs):
    return '|'.join(f"{author['last_name']}, {author['first_name']}" for author in list_of_authors_objs)

def get_cr_educational_use(course_feature_tags):
    tags = ["Curriculum/Instruction"]
    assessment_flag = any("Assignment" in tag for tag in course_feature_tags)
    professional_dev_flag = "Instructor Insights" in course_feature_tags

    if assessment_flag:
        tags.append("Assessment")

    if professional_dev_flag:
        tags.append("Professional Development")

    return "|".join(tags)

def get_cr_accessibility(course_feature_tags):
    tags = ["Visual|Textual"]
    video_flag = any("Video" in tag for tag in course_feature_tags)

    if video_flag:
        tags.append("Auditory|Caption|Transcript")

    return "|".join(tags)

def get_description_in_plain_text(description):
    stripped_markdown = markdown_to_text(description)
    stripped_html = html_to_text(stripped_markdown)
    plain_description = cleanup_curly_brackets(stripped_html)
    return plain_description

def process_single_result(result, ocw_topics_mapping):
    if result.get("runs"):
        return {
            "CR_TITLE": result["title"],
            "CR_URL": result["runs"][0]["url"],
            "CR_MATERIAL_TYPE": "Full Course",
            "CR_Media_Formats": "Text/HTML",
            "CR_ABSTRACT": get_description_in_plain_text(result["runs"][0]["description"]),
            "CR_LANGUAGE": "en",
            "CR_COU_TITLE": "Creative Commons Attribution Non Commercial Share Alike 4.0",
            "CR_PRIMARY_USER": "student|teacher",
            "CR_SUBJECT": get_cr_subjects(ocw_topics_mapping, result["topics"]),
            "CR_KEYWORDS": get_cr_keywords(result["topics"]),
            "CR_AUTHOR_NAME": get_cr_authors(result["runs"][0]["instructors"]),
            "CR_PROVIDER": "MIT",
            "CR_PROVIDER_SET": "MIT OpenCourseWare",
            "CR_COU_URL": "https://creativecommons.org/licenses/by-nc-sa/4.0/",
            "CR_COU_COPYRIGHT_HOLDER": "MIT",
            "CR_EDUCATIONAL_USE": get_cr_educational_use(result["course_feature"]),
            "CR_ACCESSIBILITY": get_cr_accessibility(result["course_feature"])
        }
    return None

def process_data(data, ocw_topics_mapping):
    return [result for result in (process_single_result(result, ocw_topics_mapping) for result in data) if result is not None]

def create_csv(source='api', output_file="ocw_oer_export.csv"):
    if source == 'api':
        api_data_json = fetch_all_data_from_api(api_url=API_URL)
    elif source == 'json':
        api_data_json = load_data_from_json("api_data.json")
    else:
        raise ValueError("Invalid source. Use 'api' or 'json'.")
    ocw_topics_mapping = create_ocw_topic_to_oer_subject_mapping()
    processed_data = process_data(api_data_json, ocw_topics_mapping)
    columns = ["CR_TITLE", "CR_URL", "CR_MATERIAL_TYPE", "CR_Media_Formats", "CR_ABSTRACT", "CR_LANGUAGE",
               "CR_COU_TITLE", "CR_PRIMARY_USER", "CR_SUBJECT", "CR_KEYWORDS", "CR_AUTHOR_NAME", "CR_PROVIDER",
               "CR_PROVIDER_SET", "CR_COU_URL", "CR_COU_COPYRIGHT_HOLDER", "CR_EDUCATIONAL_USE", "CR_ACCESSIBILITY"]
    final_df = pd.DataFrame(processed_data, columns=columns)
    final_df.to_csv(output_file, index=False)
    logger.info(f"CSV file {output_file} successfully created at present directory.")
