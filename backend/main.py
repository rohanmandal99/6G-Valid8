from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "6G-Valid8 backend is alive!"}