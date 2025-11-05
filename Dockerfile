FROM mcr.microsoft.com/playwright/python:v1.47.0-noble

# The base image already has most dependencies, just add xvfb
RUN apt-get update && apt-get install -y --no-install-recommends xvfb && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

ENV PYTHONPATH=/app/src
ENV HEADLESS=false
ENV DISPLAY=:99

CMD ["bash","-lc","xvfb-run -a --server-args='-screen 0 1280x800x24 -ac' python -m src.tasks.login"]