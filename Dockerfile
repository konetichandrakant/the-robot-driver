FROM mcr.microsoft.com/playwright/python:v1.47.0-noble

RUN apt-get update && apt-get install -y --no-install-recommends \
    xvfb \
  && apt-get clean && \
  rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Set working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project
COPY . /app

# Make src importable as a top-level package
ENV PYTHONPATH=/app/src

# Make logs unbuffered
ENV PYTHONUNBUFFERED=1

# Your utils.read_headless_mode() can use this
ENV HEADLESS=false

# Run login task
CMD ["python", "-m", "src.tasks.login"]