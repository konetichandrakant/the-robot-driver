# The Robot Driver

Agentic web automation tool that turns a **single natural-language prompt** into a sequence of **Playwright + MCP** browser actions.  
An LLM (via OpenRouter) decides what to do next on the page (navigate, click, type, etc.) until your task is completed.

---

## Features

- **Agentic Web Automation**  
  Give one prompt (e.g., *"Log in, search for a red dress and add it to cart"*).  
  The agent figures out the full sequence of browser actions.

- **Playwright + MCP**  
  Uses Playwright and the `@playwright/mcp` server to expose browser tools (navigate, click, type, etc.) to the LLM.

- **LLM via OpenRouter**  
  Model is configurable via environment variables (`OPENROUTER_MODEL`, `OPENROUTER_API_KEY`, `OPENROUTER_BASE_URL`).

- **FastAPI HTTP API**  
  Simple REST endpoint to trigger automation from any client.

- **Robust Configuration**  
  `.env`-driven settings for browser behavior, timeouts, target site, credentials, and LLM configuration.

- **Test Suite**  
  Pytest-based tests for:
  - Automation flow
  - Login task
  - MCP + LLM interaction

- **Docker-Ready**  
  Dockerfile + `docker-compose.yml` for reproducible runs and CI/CD integration.

---

## Architecture Overview

> No folder tree here – just the concepts.

- **API Layer (FastAPI)**
  - Entry point: `src/api/main.py`
  - Router: `src/api/routers/automation.py`
  - Single main endpoint:  
    `POST /api/run-automation` – runs the agentic workflow for a given user query.

- **Tasks**
  - `LLMMCPAutomation` in `src/tasks/automation_task.py`:
    - Orchestrates the LLM and Playwright MCP.
    - Maintains context across multiple steps.
    - Applies a safety limit (max iterations) to prevent infinite loops.
  - `LoginTask` (in `src/tasks/login_task.py`) encapsulates login-related steps.

- **Services**
  - `LLMService` (`src/services/llm_service.py`):
    - Wraps OpenRouter-compatible LLM calls.
    - Handles system prompt, user prompt, and response parsing.
  - `PlaywrightMCPService` (`src/services/playwright_mcp_service.py`):
    - Starts the MCP server.
    - Exposes tools like `browser_navigate`, `browser_click`, `browser_type`, etc.
    - Executes tool calls coming from the LLM.

- **Utilities**
  - `prompt_utils.py`: default system prompt + user prompt builder.
  - `automation_utils.py`: JSON extraction, validation, and action parsing helpers.
  - `config/settings.py`: central configuration using `pydantic-settings`.