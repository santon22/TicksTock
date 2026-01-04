# This Dockerfile deploys a single-container Reflex app on Railway (and similar platforms).
# It manually installs Bun to avoid curl dependency issues in minimal images.
# Uses Caddy as reverse proxy for static frontend + backend.

FROM python:3.12-slim

# Install system dependencies: Caddy, unzip (for Bun zip), wget (for download), ca-certificates (for HTTPS)
RUN apt-get update && apt-get install -y \
    caddy \
    unzip \
    wget \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Manually install Bun (latest stable as of January 2026)
# Find latest Bun version at https://github.com/oven-sh/bun/releases/latest
ENV BUN_VERSION=1.1.30  # Update if newer version available
ENV BUN_INSTALL=/usr/local
RUN wget https://github.com/oven-sh/bun/releases/download/bun-v${BUN_VERSION}/bun-linux-x64.zip && \
    unzip bun-linux-x64.zip -d /usr/local/bin && \
    rm bun-linux-x64.zip && \
    chmod +x /usr/local/bin/bun

# Verify Bun
RUN bun --version

# Port (Railway injects $PORT)
ARG PORT=8080
ENV PORT=$PORT

WORKDIR /app

# Copy requirements and install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Initialize Reflex (uses pre-installed Bun)
RUN reflex init

# Export frontend static files
RUN reflex export --frontend-only --no-zip && \
    mkdir -p /srv && \
    mv .web/_static/* /srv/ && \
    rm -rf .web

# Generate Caddyfile (proxies backend routes to localhost:8000)
RUN echo ':${PORT}\n\
encode gzip\n\
\n\
@backend {\n\
  path /_event/* /ping /_upload /_upload/*\n\
}\n\
handle @backend {\n\
  reverse_proxy localhost:8000\n\
}\n\
\n\
root * /srv\n\
file_server' > /etc/caddy/Caddyfile

# Expose port
EXPOSE $PORT

# Start backend and Caddy in parallel
CMD ["parallel", "--ungroup", "--halt", "now,fail=1", ":::", \
     "reflex run --env prod --backend-only", \
     "caddy run --config /etc/caddy/Caddyfile --adapter caddyfile"]
