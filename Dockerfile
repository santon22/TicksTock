FROM python:3.11-slim

# Install Node.js (needed for frontend build), unzip (required for Bun install), curl, and Caddy
RUN apt-get update && apt-get install -y curl gnupg unzip && \
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs && \
    apt-get install -y debian-keyring debian-archive-keyring apt-transport-https && \
    curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg && \
    curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' | tee /etc/apt/sources.list.d/caddy-stable.list && \
    apt-get update && apt-get install -y caddy && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt reflex

COPY . .

# Export frontend (adjust path if Reflex version >0.8 changes it)
RUN reflex export --frontend-only --no-zip && \
    mv .web/_static/* /srv/ && \
    rm -rf .web

EXPOSE $PORT

# Caddyfile (create this file in root)
COPY Caddyfile /etc/caddy/Caddyfile

CMD caddy start --config /etc/caddy/Caddyfile && reflex run --env prod --backend-only
