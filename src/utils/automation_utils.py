import os
from dotenv import load_dotenv

load_dotenv(".env")

def get_website():
    if os.getenv("WEBSITE_URL") is None:
        raise ValueError("WEBSITE_URL environment variable is not set.")
    return os.getenv("WEBSITE_URL")
    
def get_user_credentials():
    if os.getenv("USER_EMAIL") is None or os.getenv("USER_PASSWORD") is None:
        raise ValueError("USER_EMAIL or USER_PASSWORD environment variable is not set.")
    return os.getenv("USER_EMAIL"), os.getenv("USER_PASSWORD")

def get_llm_url():
    if os.getenv("OPENROUTER_BASE_URL") is None:
        raise ValueError("OPENROUTER_BASE_URL environment variable is not set.")
    return os.getenv("OPENROUTER_BASE_URL")

def get_model():
    if os.getenv("OPENROUTER_MODEL") is None:
        raise ValueError("OPENROUTER_MODEL environment variable is not set.")
    return os.getenv("OPENROUTER_MODEL")

def get_llm_api_key():
    if os.getenv("OPENROUTER_API_KEY") is None:
        raise ValueError("OPENROUTER_API_KEY environment variable is not set.")
    return os.getenv("OPENROUTER_API_KEY")