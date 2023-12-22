"""
Module for interacting with the MIT OpenCourseWare API.
"""
import logging
import requests
from retry import retry

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@retry(tries=3, delay=2, logger=logger)
def make_request(next_page, page_size):
    """
    Make a request to the API with retry logic.
    """
    return requests.get(next_page, params={"limit": page_size}, timeout=60)


def paginated_response(api_url, page_size=100):
    """
    Generate paginated responses from the API.
    """
    next_page = api_url
    while next_page:
        response = make_request(next_page, page_size)
        data = response.json()
        next_page = data.get("next")
        yield data


def extract_data_from_api(api_url):
    """Extract all data from the MIT OpenCourseWare API."""
    api_data = []
    local_objects_count = 0  # Local count of objects accumulated
    total_objects_count = None  # Total count of objects
    pages = paginated_response(api_url)

    for page in pages:
        page_results = page.get("results", [])
        api_data.extend(page_results)

        # Update the local count
        local_objects_count += len(page_results)

        # Update the total count if not set
        if total_objects_count is None and "count" in page:
            total_objects_count = page["count"]

        # Calculate the progress percentage
        if total_objects_count is not None and total_objects_count != 0:
            progress_percentage = (local_objects_count / total_objects_count) * 100
            logger.info("API loaded - Progress: %.2f%%", progress_percentage)

    return api_data
