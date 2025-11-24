from fastapi import FastAPI
from src.api.routers.automation import router as automation_router

app = FastAPI(
    title="The Robot Driver API",
    description="""
    The Robot Driver API provides intelligent web automation capabilities powered by AI.

    This API allows you to execute complex web automation tasks by simply describing what you want to accomplish in natural language. The system uses advanced LLM reasoning and browser automation to perform tasks like:

    * **Web Scraping**: Extract data from websites
    * **Form Filling**: Automatically complete and submit forms
    * **Navigation**: Browse websites and interact with elements
    * **Data Entry**: Input data into web applications
    * **Testing**: Perform automated UI testing

    The API integrates with OpenRouter for language model capabilities and uses Playwright for reliable browser automation.
    """,
    version="1.0.0",
    contact={
        "name": "The Robot Driver Team",
        "email": "support@robotdriver.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

app.include_router(automation_router, prefix="/api", tags=["automation"])
