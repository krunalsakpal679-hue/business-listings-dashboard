from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import listings, dashboard

app = FastAPI(
    title="Business Listings Dashboard API",
    description="Backend API for managing and querying business listings statistics",
    version="1.0.0"
)

# Configure CORS Middleware
origins = [
    "http://localhost:5173", # Vite React local server default
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Allow all standard HTTP methods
    allow_headers=["*"], # Allow all headers
)

# Register routers
app.include_router(listings.router)
app.include_router(dashboard.router)

@app.get("/")
def read_root():
    return {
        "status": "online",
        "message": "Welcome to the Business Listings Dashboard API. Refer to /docs for endpoint usage."
    }
