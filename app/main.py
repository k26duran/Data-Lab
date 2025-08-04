from fastapi import FastAPI
from .routers import upload, metrics

app = FastAPI(title="DB Migration API")

app.include_router(upload.router)
app.include_router(metrics.router)

@app.get("/")
def read_root():
    return {"message": "API Running"}