from playwright.async_api import async_playwright

class Login:
    
    # Initialize with website URL and user credentials
    def __init__(self, website_url: str = "", username: str = "", password: str = "", headless: bool = True):
        self.website_url = website_url
        self.username = username
        self.password = password
        self.headless = headless
    
    # execute function performs the login task
    async def execute(self) -> str:
        print("Login requested.")

        async with async_playwright() as p:
            browser = None
            try:
                # Create browser instance (to have a real time view of the actions, headless is set to False)
                browser = await p.chromium.launch(headless=self.headless, slow_mo=600)
                page = await browser.new_page()

                # Navigate to the URL from environment variable
                await page.goto(self.website_url, wait_until="domcontentloaded")

                # Open the login page from the header link
                await page.get_by_role("link", name="Signup / Login").click()

                # Perform login using credentials from environment variables
                await page.fill('input[data-qa="login-email"]', self.username)  # fill in email field
                await page.fill('input[data-qa="login-password"]', self.password)  # fill in password field
                await page.click('button[data-qa="login-button"]')  # submit the login form
                await page.wait_for_load_state('networkidle')  # wait for navigation to complete

            except Exception as e:
                # Print any exception that occurs during the login process and raise to make the test as failed
                print(f"An error occurred during login: {e}")
                raise e
            
            finally:
                # Always close browser instance, even if an error occurs
                if browser:
                    await browser.close()
                    print("Browser closed successfully.")

            print("Login task completed.")