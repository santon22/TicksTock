# This Dockerfile deploys a single-container Reflex app on platforms like Railway.
# It uses Caddy as reverse proxy and manually installs Bun to avoid installer issues.
# Tested for Reflex versions ~0.5+ (as of January 2026).

FROM python:3.12-slim AS builder

# Install build dependencies: wget, unzip, ca-certificates
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Manually install latest Bun (as of Jan 2026: 1.3.x; check https://github.com/oven-sh/bun/releases for updates)
ENV BUN_VERSION=1.3.4
RUN wget https://github.com/oven-sh/bun/releases/download/bun-v${BUN_VERSION}/bun-linux-x64.zip && \
    unzip bun-linux-x64.zip -d /usr/local/bin && \
    rm bun-linux-x64.zip && \
    chmod +x /usr/local/bin/bun

# Verify Bun
RUN bun --version

WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Initialize Reflex (uses pre-installed Bun)
RUN reflex init

# Export frontend static files (path valid for recent Reflex versions)
RUN reflex export --frontend-only --no-zip && \
    mkdir -p /srv && \
    mv .web/_static/* /srv/ && \
    rm -rf .web

# Final runtime stage
FROM python:3.12-slim

# Install runtime dependencies: Caddy and parallel
RUN apt-get update && apt-get install -y \
    caddy \
    parallel \
    && rm -rf /var/lib/apt/lists/*

# Port (Railway injects $PORT)
ARG PORT=8080
ENV PORT=$PORT

WORKDIR /app

# Copy app and static files from builder
COPY --from=builder /app /app
COPY --from=builder /srv /srv

# Generate Caddyfile dynamically
RUN echo ":${PORT}\n\
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
file_server" > /etc/caddy/Caddyfile

EXPOSE $PORT

# Start both Reflex backend and Caddy
CMD ["parallel", "--ungroup", "--halt", "now,fail=1", ":::", \
     "reflex run --env prod --backend-only", \
     "caddy run --config /etc/caddy/Caddyfile --adapter caddyfile"]
