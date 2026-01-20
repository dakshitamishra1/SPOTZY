from fastapi import FastAPI
from app.auth.routes import router as auth_router

app = FastAPI(title="Spotzy Authentication API")

app.include_router(auth_router)

@app.get("/")
def home():
    return {"message": "Spotzy API Running Successfully!"}
