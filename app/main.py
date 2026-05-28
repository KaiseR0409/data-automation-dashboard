from fastapi import  FastAPI
from app.routes.analytics_routes import router as analytics_router
from app.routes.upload_routes import router as upload_router
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from pathlib import Path

import os

env_path = Path(__file__).resolve().parent / ".env"

load_dotenv(dotenv_path=env_path)

PAGE_URL = os.getenv("PAGE_URL")

app = FastAPI(
    title="Data Automation API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        PAGE_URL
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(upload_router)
app.include_router(analytics_router)