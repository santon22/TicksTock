import reflex as rx
import os

railway_domain = "RAILWAY_PUBLIC_DOMAIN"

config = rx.Config(
    app_name="Ticks_Tock",
    telemetry_enabled=False,
    frontend_port=3000,
    backend_port=8000,
    api_url=f'https://{os.environ.get(railway_domain)}/backend' if railway_domain in os.environ else "http://127.0.0.1:8000"
)
