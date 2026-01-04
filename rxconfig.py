import reflex as rx
import os

config = rx.Config(
    app_name="Ticks_Tock",,  # e.g., folder name of your app.py
    api_url=f"https://{os.environ.get('RAILWAY_PUBLIC_DOMAIN', '')}" if os.environ.get('RAILWAY_PUBLIC_DOMAIN') else "http://localhost:8000",
    telemetry_enabled=False,
)
