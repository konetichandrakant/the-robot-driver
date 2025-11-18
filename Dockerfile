FROM mcr.microsoft.com/playwright/python:v1.47.0-noble

# Install xvfb + nodejs/npm
RUN apt-get update && apt-get install -y --no-install-recommends \
    xvfb \
    nodejs \
    npm \
  && apt-get clean && \
  rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Work in /app
WORKDIR /app

# Python deps first (so we cache them if requirements.txt doesn't change)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project
COPY . /app

# Pre-install @playwright/mcp and Chrome for Playwright
# - Create package.json if it doesn't exist
# - Install @playwright/mcp locally
# - Install the Chrome browser distribution Playwright expects
RUN if [ ! -f package.json ]; then npm init -y; fi && \
    npm install @playwright/mcp@0.0.47 && \
    npx playwright install chrome

# Make src importable as a top-level package
ENV PYTHONPATH=/app/src
ENV PYTHONUNBUFFERED=1
ENV HEADLESS=false

# Default command: run the login task (you can override with pytest)
CMD ["python", "-m", "src.tasks.login"]
