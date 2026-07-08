from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database.connection import engine, Base
from app.routes import auth, ai

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="CookWise AI API")

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "https://cooking-agent-front.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(auth.router)
app.include_router(ai.router)

@app.get("/")
def root():
    return {"message": "CookWise AI Backend is running"}
