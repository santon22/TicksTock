config = rx.Config(
    app_name="web",
    title="title",
    description="desc",
    backend_port=8000,
    frontend_port=3000,
    db_url=DATABASE_URL,
    cors_allowed_origins=[
    "http://127.0.0.1:3000",
    f"https://{RAILWAY_PUBLIC_DOMAIN}",
    ],
    api_url=(
        f"https://{RAILWAY_PUBLIC_DOMAIN}/backend"
        if RAILWAY_PUBLIC_DOMAIN  
        else "http://127.0.0.1:8000"
    )
)
