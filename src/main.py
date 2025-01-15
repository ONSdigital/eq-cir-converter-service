import fastapi

from src.routers import schema_router

app = fastapi.FastAPI()


# Simple hello world endpoint
@app.get("/")
def index() -> dict:
    return {"message": "Hello World!"}


app.include_router(schema_router.router)
