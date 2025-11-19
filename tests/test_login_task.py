from src.tasks.login import Login
from src.config import WEBSITE_URL, USER_CREDENTIALS, BROWSER_HEADLESS
import pytest

@pytest.mark.asyncio
async def test_login():
    website_url = WEBSITE_URL
    username, password = USER_CREDENTIALS
    headless = BROWSER_HEADLESS

    # Run the login function
    login_task = Login(website_url, username, password, headless)
    response = await login_task.execute()

    # If no exceptions were raised, we assume the test passed
    assert (response == "Login task completed.")