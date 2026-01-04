FROM python:3.11-slim

# Install Node.js (for frontend build) and Caddy
RUN apt-get update && apt-get install -y curl gnupg && \
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs && \
    apt-get install -y debian-keyring debian-archive-keyring apt-transport-https && \
    curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg && \
    curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' | tee /etc/apt/sources.list.d/caddy-stable.list && \
    apt-get update && apt-get install -y caddy && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install -r requirements.txt reflex

# Copy code
COPY . .

# Export frontend
RUN reflex export --frontend-only && mv .web/_static /srv && rm -rf .web

# Expose port (Railway uses $PORT)
EXPOSE $PORT

# Start Caddy + Reflex backend
CMD caddy start --config /app/Caddyfile & reflex run --env prod --backend-only
