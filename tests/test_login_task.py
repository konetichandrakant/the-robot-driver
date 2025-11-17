from src.tasks.login import Login
from src.utils.automation_utils import get_website, get_user_credentials, get_headless_mode
import pytest

@pytest.mark.asyncio
async def test_login():
    """Test the login function with mock credentials."""
    website_url = get_website()
    username, password = get_user_credentials()
    headless = get_headless_mode()
    
    print(website_url, username, password, headless)

    # Run the login function
    login_task = Login()
    response = await login_task.execute(website_url, username, password, headless)

    # If no exceptions were raised, we assume the test passed
    assert (response == "Login task completed.")