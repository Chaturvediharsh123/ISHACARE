from fastapi import FastAPI
from routes.analyze import router

app = FastAPI(title="AI Health Monitoring System")

app.include_router(router)

@app.get("/")
def home():
    return {"message": "Health AI Pipeline Running 🚀"}