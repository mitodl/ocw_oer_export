"""
Module for interacting with the MIT OpenCourseWare API.
"""
import logging
import requests
from retry import retry

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@retry(tries=3, delay=2, logger=logger)
def fetch_data_from_api(api_url, limit=100):
    """Fetch all data from the MIT OpenCourseWare API."""
    api_data = []
    local_count = 0  # Local count of objects accumulated

    try:
        while api_url:
            response = requests.get(api_url, params={"limit": limit}, timeout=600)
            response.raise_for_status()
            data = response.json()
            results = data.get("results", [])
            api_data.extend(results)
            api_url = data.get("next")

            # Update the local count
            local_count += len(results)

            # Calculate the progress percentage
            progress_percentage = (local_count / data.get("count", 1)) * 100
            logger.info("%% API loaded - Progress: %.2f%%\r", progress_percentage)

    except requests.RequestException as e:
        logger.error("Error fetching data from API: %s", e)

    return api_data
