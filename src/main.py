import fastapi

app = fastapi.FastAPI()


@app.get("/")
def index() -> dict:
    return {"message": "Hello World!"}
