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

# This layer will be reused as long as everything above doesn't change.
RUN npm init -y && \
    npm install @playwright/mcp@0.0.47 && \
    npx playwright install chrome

# Python deps (requirements.txt)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ---- App source code (changes often, last) ----
COPY . /app