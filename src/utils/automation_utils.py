import os
from functools import lru_cache
from dotenv import load_dotenv

load_dotenv()

class ConfigCache:
    """Cache for environment variables to improve performance."""
    _cache = {}

    @classmethod
    def get_cached_env(cls, key: str, required: bool = True):
        """Get cached environment variable or raise error if required and not set."""
        if key not in cls._cache:
            value = os.getenv(key)
            if required and value is None:
                raise ValueError(f"{key} environment variable is not set.")
            cls._cache[key] = value
        return cls._cache[key]

@lru_cache(maxsize=None)
def get_website() -> str:
    """Get website URL from environment with caching."""
    return ConfigCache.get_cached_env("WEBSITE_URL")

def get_user_credentials() -> tuple[str, str]:
    """
    Get user credentials from environment.

    Returns:
        tuple: (email, password) for user authentication

    Note: Currently used in tests and login tasks for authentication.
    """
    email = ConfigCache.get_cached_env("USER_EMAIL")
    password = ConfigCache.get_cached_env("USER_PASSWORD")
    return email, password

@lru_cache(maxsize=None)
def get_llm_url() -> str:
    """Get LLM URL from environment with caching."""
    return ConfigCache.get_cached_env("OPENROUTER_BASE_URL")

@lru_cache(maxsize=None)
def get_model() -> str:
    """Get model name from environment with caching."""
    return ConfigCache.get_cached_env("OPENROUTER_MODEL")

@lru_cache(maxsize=None)
def get_llm_api_key() -> str:
    """Get LLM API key from environment with caching."""
    return ConfigCache.get_cached_env("OPENROUTER_API_KEY")

@lru_cache(maxsize=None)
def get_headless_mode() -> bool:
    """
    Get headless mode setting from environment with caching.

    Returns:
        bool: True if browser should run in headless mode

    Note: Used in tests and browser automation for headless configuration.
    """
    headless_value = ConfigCache.get_cached_env("BROWSER_HEADLESS")
    return headless_value.lower() in ('true', '1', 'yes')