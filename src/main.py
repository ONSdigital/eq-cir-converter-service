import fastapi

app = fastapi.FastAPI()


# Simple hello world endpoint
@app.get("/")
def index() -> dict:
    return {"message": "Hello World! - Test Cloud Build!"}
