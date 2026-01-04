import reflex as rx

config = rx.Config(
    app_name="Ticks_Tock",
    api_url=f"https://{{{{RAILWAY_STATIC_URL}}}}/api",
)
