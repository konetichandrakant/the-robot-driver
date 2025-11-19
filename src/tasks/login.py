from playwright.async_api import async_playwright

class Login:
    def __init__(self, website_url: str = "", username: str = "", password: str = "", headless: bool = True):
        self.website_url = website_url
        self.username = username
        self.password = password
        self.headless = headless
    
    async def execute(self) -> str:
        print("Login requested.")
        
        async with async_playwright() as p:
            # Create browser instance (to have a real time view of the actions, headless is set to False)
            browser = await p.chromium.launch(headless=self.headless, slow_mo=600)
            page = await browser.new_page()
            
            # Navigate to the URL from environment variable
            await page.goto(self.website_url, wait_until="domcontentloaded")
            
            # Open the login page from the header link
            await page.get_by_role("link", name="Signup / Login").click()

            # Perform login using credentials from environment variables
            try:
                await page.fill('input[data-qa="login-email"]', self.username)  # fill in email field
                await page.fill('input[data-qa="login-password"]', self.password)  # fill in password field
                await page.click('button[data-qa="login-button"]')  # submit the login form
                await page.wait_for_load_state('networkidle')  # wait for navigation to complete
                print("Login attempted.")
            except Exception as e:
                print(f"An error occurred during login: {e}")
            
            # Keep the browser open a bit so you can see the result
            await page.wait_for_timeout(3000)

            # Close browser instance
            await browser.close()
            
            return "Login task completed."