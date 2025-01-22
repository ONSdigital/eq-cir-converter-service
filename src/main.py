import fastapi

from src.routers import schema_router

app = fastapi.FastAPI()

app.include_router(schema_router.router)
