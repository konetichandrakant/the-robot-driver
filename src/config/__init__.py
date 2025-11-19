# Direct module-level variables
from .settings import (
    Config,
    config,
    WEBSITE_URL,
    USER_EMAIL,
    USER_PASSWORD,
    USER_CREDENTIALS,
    OPENROUTER_BASE_URL,
    OPENROUTER_MODEL,
    OPENROUTER_API_KEY,
    BROWSER_HEADLESS,
    APP_NAME,
    DEBUG,
    BROWSER_SLOW_MO,
    BROWSER_TIMEOUT,
    HOST,
    PORT,
    DEFAULT_WAIT_TIMEOUT,
    SCREENSHOT_ON_FAILURE,
)

__all__ = [
    # Config class and instance
    "Config",
    "config",

    # Core automation variables
    "WEBSITE_URL",
    "USER_EMAIL",
    "USER_PASSWORD",
    "USER_CREDENTIALS",
    "OPENROUTER_BASE_URL",
    "OPENROUTER_MODEL",
    "OPENROUTER_API_KEY",
    "BROWSER_HEADLESS",

    # Additional configuration variables
    "APP_NAME",
    "DEBUG",
    "BROWSER_SLOW_MO",
    "BROWSER_TIMEOUT",
    "HOST",
    "PORT",
    "DEFAULT_WAIT_TIMEOUT",
    "SCREENSHOT_ON_FAILURE",
]