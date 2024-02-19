"""
Module for loading environment settings and setting the API base URL based on the current environment.
"""
import os
from dotenv import load_dotenv
from .constants import API_BASE_URLS

load_dotenv()

environment_key = os.getenv("ENVIRONMENT", "PRODUCTION").upper()
API_URL = API_BASE_URLS.get(environment_key)
