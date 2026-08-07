from fastapi import FastAPI

app = FastAPI(title="Business Listings Dashboard API")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Business Listings Dashboard API"}
