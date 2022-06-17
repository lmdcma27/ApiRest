from fastapi import FastAPI
from routes.user import user

app = FastAPI(
    title="Primera API",
    description="descripción de la prime api",
    openapi_tags=[{
        "name": "users",
        "description": "users routes"
    }]
)

app.include_router(user)

