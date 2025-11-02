# The Robot Driver

A powerful Playwright-based automation framework with MCP (Model Context Protocol) integration for intelligent web automation.

## Features

- **Browser Automation**: Full Playwright integration for reliable web automation
- **MCP Integration**: AI-powered automation through Model Context Protocol
- **Modular Architecture**: Clean separation of concerns with service-based design
- **Configuration Management**: Flexible settings with environment variable support
- **Error Handling**: Comprehensive error handling and logging
- **Screenshot Support**: Automatic screenshot capture on failures
- **Docker Support**: Ready-to-use Docker configuration

## Project Structure

```
the-robot-driver/
├── src/                          # Main source code
│   ├── config/                   # Configuration management
│   │   └── settings.py          # Application settings
│   ├── services/                 # Core services
│   │   ├── browser_service.py   # Browser automation service
│   │   ├── mcp_service.py       # MCP/AI integration service
│   │   ├── automation_service.py # Main automation orchestrator
│   │   └── ai_service.py        # AI-powered features
│   ├── tasks/                    # Automation tasks
│   │   ├── signup.py           # User signup automation
│   │   └── llm_automation.py   # LLM-powered automation
│   └── utils/                    # Utility modules
│       └── logger.py            # Logging configuration
├── tests/                        # Test suite
├── logs/                         # Application logs (auto-created)
├── screenshots/                  # Screenshots (auto-created)
├── playwright_mcp_automation.py # Main entry point
├── requirements.txt              # Python dependencies
├── Dockerfile                   # Docker configuration
├── docker-compose.yml          # Docker Compose setup
├── .env.example                # Environment variables template
└── README.md                   # This file
```

## Quick Start

### Using Docker (Recommended)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd the-robot-driver
   ```

2. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

3. **Build and run**
   ```bash
   docker-compose up --build
   ```

### Local Development

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   playwright install
   ```

2. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

3. **Run the application**
   ```bash
   python playwright_mcp_automation.py
   ```

## Configuration

The application uses environment variables for configuration. Copy `.env.example` to `.env` and modify as needed:

```bash
# Application Settings
APP_NAME=The Robot Driver
DEBUG=false

# Browser Settings
BROWSER_HEADLESS=false
BROWSER_SLOW_MO=100
BROWSER_TIMEOUT=30000

# Server Settings
HOST=0.0.0.0
PORT=8000

# MCP Settings (Optional)
MCP_SERVER_URL=http://localhost:8080
MCP_API_KEY=your_api_key_here
```

## Usage Examples

### Basic Web Automation

```python
from services.automation_service import AutomationService
from config.settings import Settings

async def example_automation():
    settings = Settings()
    automation_service = AutomationService(browser_service, mcp_service, settings)

    task_config = {
        "type": "web_automation",
        "url": "https://example.com",
        "actions": [
            {"type": "fill", "selector": "input[name='username']", "value": "testuser"},
            {"type": "fill", "selector": "input[name='password']", "value": "password123"},
            {"type": "click", "selector": "button[type='submit']"},
            {"type": "wait", "timeout": 2000},
            {"type": "screenshot", "filename": "login_success.png"}
        ]
    }

    result = await automation_service.execute_task(task_config)
    print(result)
```

### Page Analysis with AI

```python
task_config = {
    "type": "page_analysis",
    "url": "https://example.com"
}

result = await automation_service.execute_task(task_config)
if result["success"]:
    print("Page analysis:", result["analysis"])
```

## Testing

Run the test suite:

```bash
pytest tests/
```

## Docker Configuration

The project includes Docker support with:
- **Dockerfile**: Multi-stage build for production
- **docker-compose.yml**: Development setup with volume mounting
- **.dockerignore**: Optimized build context

## Development

### Adding New Services

1. Create service file in `src/services/`
2. Implement the service class with `start()` and `stop()` methods
3. Register in main application if needed

### Adding New Tasks

1. Create task file in `src/tasks/`
2. Implement async functions with proper error handling
3. Add logging for debugging

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is licensed under the MIT License.
