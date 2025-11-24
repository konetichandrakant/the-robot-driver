from src.tasks.login_task import Login
from src.config import WEBSITE_URL, USER_CREDENTIALS, BROWSER_HEADLESS, BROWSER_SLOW_MO
import pytest

@pytest.mark.asyncio
async def test_login():
    try:
        username, password = USER_CREDENTIALS
        
        # Run the login function
        login_task = Login(website_url=WEBSITE_URL, username=username, password=password, headless=BROWSER_HEADLESS, slow_mo=BROWSER_SLOW_MO)
        await login_task.execute()
        
        # If no exceptions were raised, we assume the test passed
        assert True
        
    except Exception as e:
        # If exceptions were raised, we assume the test is failed
        assert False