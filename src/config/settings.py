from typing import Tuple
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

load_dotenv()

class Config(BaseSettings):
    # Application Settings
    app_name: str = Field(default="The Robot Driver", alias="APP_NAME")
    debug: bool = Field(default=False, alias="DEBUG")

    # Website and application settings
    website_url: str = Field(alias="WEBSITE_URL")

    # User credentials
    user_email: str = Field(alias="USER_EMAIL")
    user_password: str = Field(alias="USER_PASSWORD")

    # LLM settings
    openrouter_base_url: str = Field(alias="OPENROUTER_BASE_URL")
    openrouter_model: str = Field(alias="OPENROUTER_MODEL")
    openrouter_api_key: str = Field(alias="OPENROUTER_API_KEY")

    # Browser settings
    browser_headless: bool = Field(default=False, alias="BROWSER_HEADLESS")
    browser_slow_mo: int = Field(default=100, alias="BROWSER_SLOW_MO")
    browser_timeout: int = Field(default=30000, alias="BROWSER_TIMEOUT")

    # Server settings
    host: str = Field(default="0.0.0.0", alias="HOST")
    port: int = Field(default=8000, alias="PORT")

    # Automation settings
    default_wait_timeout: int = Field(default=5000, alias="DEFAULT_WAIT_TIMEOUT")
    screenshot_on_failure: bool = Field(default=True, alias="SCREENSHOT_ON_FAILURE")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",  # This will ignore extra fields instead of raising errors
        case_sensitive=False,
    )

    @property
    def user_credentials(self) -> Tuple[str, str]:
        """Get user credentials as a tuple."""
        return (self.user_email, self.user_password)


# Load configuration
config = Config()

# Direct module-level variables for import like: from src.config import WEBSITE_URL
WEBSITE_URL = config.website_url
USER_EMAIL = config.user_email
USER_PASSWORD = config.user_password
USER_CREDENTIALS = config.user_credentials
OPENROUTER_BASE_URL = config.openrouter_base_url
OPENROUTER_MODEL = config.openrouter_model
OPENROUTER_API_KEY = config.openrouter_api_key
BROWSER_HEADLESS = config.browser_headless

# Additional configuration variables available for import
APP_NAME = config.app_name
DEBUG = config.debug
BROWSER_SLOW_MO = config.browser_slow_mo
BROWSER_TIMEOUT = config.browser_timeout
HOST = config.host
PORT = config.port
DEFAULT_WAIT_TIMEOUT = config.default_wait_timeout
SCREENSHOT_ON_FAILURE = config.screenshot_on_failure