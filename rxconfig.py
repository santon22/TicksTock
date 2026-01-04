import reflex as rx
import os

railway_domain = "RAILWAY_PUBLIC_DOMAIN"

class ReflextemplateConfig(rx.Config):
    pass

config = ReflextemplateConfig(
    app_name="app",
    telemetry_enabled=False,
    frontend_port=3000,  # default frontend port
    backend_port=8000,   # default backend port
    plugins=[
        rx.plugins.sitemap.SitemapPlugin(),  # Explicitly added to silence the warning and enable sitemap.xml
    ],
    # Conditional api_url from original template (kept for custom domain support)
    # Note: On Railway without custom domain, this falls back to local. With custom domain, uses /backend route.
    api_url=f'https://{os.environ[railway_domain]}/backend' if railway_domain in os.environ else "http://127.0.0.1:8000",
)
