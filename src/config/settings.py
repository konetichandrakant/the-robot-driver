"""
Configuration settings for The Robot Driver.
"""

import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    # Application settings
    app_name: str = "The Robot Driver"
    version: str = "1.0.0"
    debug: bool = False

    # Browser settings
    browser_headless: bool = False
    browser_slow_mo: int = 100
    browser_timeout: int = 30000

    # Server settings
    host: str = "0.0.0.0"
    port: int = 8000

    # MCP settings
    mcp_server_url: Optional[str] = None
    mcp_api_key: Optional[str] = None

    # Automation settings
    default_wait_timeout: int = 5000
    screenshot_on_failure: bool = True

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"