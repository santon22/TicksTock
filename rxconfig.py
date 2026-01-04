import reflex as rx
import os

config = rx.Config(
    app_name="app", 
    telemetry_enabled=False,
    plugins=[rx.plugins.sitemap.SitemapPlugin()],
)
