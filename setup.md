# Docker Setup – The Robot Driver

Here's my Docker setup for the Robot Driver project using WSL2.
I run these commands in my **WSL terminal (Ubuntu)** with Docker Desktop + X server on Windows.

## 1. Display Environment Configuration 🖥️

Configure X11 display forwarding for GUI apps in Docker so **Playwright** can show a real browser (when not headless).

```bash
export DISPLAY=$(grep -m 1 nameserver /etc/resolv.conf | awk '{print $2}'):0
````

(Sometimes needed for graphics issues)

```bash
export LIBGL_ALWAYS_INDIRECT=1
```

-----

## 2\. Navigate to Project Directory 📂

Update this path if your project is in a different location.

```bash
cd ../parent-directory/the-robot-driver
```

-----

## 3\. Environment File (.env) ⚙️

I keep a **`.env`** in the project root with all config.

> ```text
> APP_NAME=The Robot Driver
> DEBUG=false
> BROWSER_HEADLESS=false
> BROWSER_SLOW_MO=100
> BROWSER_TIMEOUT=30000
> HOST=0.0.0.0
> PORT=8000
> DEFAULT_WAIT_TIMEOUT=5000
> SCREENSHOT_ON_FAILURE=true
> WEBSITE_URL=your-website-url
> USER_EMAIL=your-email@example.com
> USER_PASSWORD=your-password
> OPENROUTER_API_KEY=your-openrouter-api-key
> OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
> OPENROUTER_MODEL=meta-llama/llama-3.3-70b-instruct:free
> ```

Example:

```bash
nano .env
```

-----

## 4\. Build Docker Image 🏗️

(Optional) Clean up previous build cache

```bash
docker builder prune -f
```

Build the Docker image with **no cache** so I get latest changes

```bash
docker build --no-cache -t the-robot-driver-app .
```

-----

## 5\. Run Tests with Docker Compose 🧪

**`docker-compose.yml`** is configured with:

  * service: **`automation_test`** -\> runs `tests/test_automation_api.py`
  * service: **`login_task_test`** -\> runs `tests/test_login_task.py` (with GUI/X11 support)

Both services mount `./src`, `./tests`, and `.env` into the container.

Run the automation API tests (headless by default)

```bash
docker compose run --rm automation_test
```

Run the login task tests (GUI / browser tests if **`BROWSER_HEADLESS=false`**)

```bash
docker compose run --rm login_task_test
```

-----

## 6\. Run the FastAPI Server using docker-compose 🚀

I already have an **`api`** service defined in `docker-compose.yml`.
To bring up the API container, I just run:

```bash
docker compose up api
```

Now I can open:

  * **`http://localhost:8000/docs`** (FastAPI Swagger UI)
  * **`POST http://localhost:8000/api/run-automation`**

## 7\. Quick Troubleshooting 🛠️

  * **429 / rate limit errors from OpenRouter:**

      * Check `OPENROUTER_API_KEY`
      * Check daily free limit / credits
      * Try a lighter/free model in `OPENROUTER_MODEL`

  * **GUI doesn't show up for login\_task\_test:**

      * Ensure **X server is running on Windows** (VcXsrv/Xming)
      * Verify `DISPLAY` is set in WSL: `echo $DISPLAY`
      * Make sure `docker-compose.yml` mounts `/tmp/.X11-unix`

  * **Tests don't pick up new code changes:**

      * `docker-compose` mounts `./src` and `./tests`, so usually no rebuild needed unless the base image changed.
      * If `Dockerfile` / base image changed, rebuild with `--no-cache`.

  * **Browser fails to start:**

      * Check `BROWSER_HEADLESS` in `.env`
      * Try headless mode first: `BROWSER_HEADLESS=true`
      * Rebuild the image if Playwright version changed.
