import playwright.sync_api as pw
import pythondotenv as dotenv

def login(page: pw.Page, username: str, password: str) -> None:
    """
    Logs into a website using the provided username and password.

    Args:
        page (pw.Page): The Playwright page object.
        username (str): The username for login.
        password (str): The password for login.
    """
    # Navigate to the login page
    page.goto("https://example.com/login")

    # Fill in the username and password fields
    page.fill("input[name='username']", username)
    page.fill("input[name='password']", password)

    # Click the login button
    page.click("button[type='submit']")

    # Wait for navigation to complete after login
    page.wait_for_load_state("networkidle")