FROM mcr.microsoft.com/playwright/python:v1.47.0-noble

# Install xvfb + nodejs/npm (for Playwright MCP Node server)
RUN apt-get update && apt-get install -y --no-install-recommends \
    xvfb \
    nodejs \
    npm \
  && apt-get clean && \
  rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Work in /app
WORKDIR /app

# Install Python dependencies FIRST (includes playwright package)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Node.js dependencies
RUN npm init -y && \
    npm install @playwright/mcp@latest

# Install browsers for both Python and Node.js playwright (now both available)
RUN npx playwright install chrome && \
    playwright install chromium && \
    playwright install-deps

# Set Playwright browser path environment variable
ENV PLAYWRIGHT_BROWSERS_PATH=/ms-playwright

# ---- App source code (changes often, last) ----
COPY . /app