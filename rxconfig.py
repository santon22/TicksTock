import reflex as rx
import os

# Railway sets RAILWAY_PUBLIC_DOMAIN at runtime
railway_domain = os.environ.get("RAILWAY_PUBLIC_DOMAIN")

config = rx.Config(
    app_name="Ticks_Tock",
    telemetry_enabled=False,
    frontend_port=3000,
    backend_port=8000,
    # During build, railway_domain is None → use local backend
    # At runtime on Railway, use the public domain with /backend prefix
    api_url=f"https://{railway_domain}/backend" if railway_domain else "http://127.0.0.1:8000",
)
