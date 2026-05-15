from fastapi import FastAPI
from webhook import router

app = FastAPI()

# Include webhook routes
app.include_router(router)

@app.get("/")
def home():
    return {"message": "Server Running Successfully"}