# This Dockerfile deploys a single-container Reflex app on platforms like Railway.
# It serves static frontend via Caddy and proxies backend requests.

FROM python:3.12-slim

# Port (Railway uses $PORT, default to 8080 if not set)
ARG PORT=8080
ENV PORT=$PORT

# Install system dependencies: Caddy, unzip (required for Bun), and parallel (optional but useful)
RUN apt-get update && apt-get install -y \
    caddy \
    unzip \
    parallel \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Initialize Reflex and export frontend static files
RUN reflex init
RUN reflex export --frontend-only --no-zip && \
    mv .web/_static/* /srv/ && \
    rm -rf .web

# Create Caddyfile for reverse proxy
RUN echo ':${PORT}\n\
encode gzip\n\
@backend_routes path /_event/* /ping /_upload /_upload/*\n\
handle @backend_routes {\n\
  reverse_proxy localhost:8000\n\
}\n\
root * /srv\n\
file_server' > /etc/caddy/Caddyfile

# Expose port
EXPOSE $PORT

# Start both backend and Caddy using parallel
CMD ["parallel", "--ungroup", "--halt", "now,fail=1", ":::", \
     "reflex run --env prod --backend-only", \
     "caddy run --config /etc/caddy/Caddyfile --adapter caddyfile"]
