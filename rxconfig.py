import reflex as rx
import os

config = rx.Config(
    app_name="myapp",  # Replace with your actual folder name, e.g., "TicksTock" if your app code is in TicksTock/TicksTock.py
    telemetry_enabled=False,
    plugins=[
        rx.plugins.sitemap.SitemapPlugin(),  # Explicitly add to silence the warning (recommended for SEO)
    ],
    # No need to set frontend_port or backend_port — Brody's template with Caddy handles this automatically
    # api_url is only needed during frontend compile if separated; in Brody's single-process setup on Railway, leave default (empty) so it uses relative paths (works perfectly behind Caddy proxy)
    # Do NOT set api_url here — it would force absolute URLs and break websocket connections on Railway
)
