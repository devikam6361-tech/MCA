
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from database import Base, engine
import models

from routers import students, labs, attendance, faces


BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create database tables when the application starts.
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="SmartLab AI API",
    description=(
        "Backend API for student management, "
        "AI-assisted lab attendance, and lab sessions."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

# Allow requests from the React development server.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://mca-frontend-5t5h.onrender.com",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve uploaded student photos.
app.mount(
    "/uploads",
    StaticFiles(directory=str(UPLOAD_DIR)),
    name="uploads",
)

# Register the student API.
app.include_router(students.router, prefix="/api/v1")
app.include_router(labs.router, prefix="/api/v1")
app.include_router(attendance.router, prefix="/api/v1")
app.include_router(faces.router, prefix="/api/v1")


@app.get("/")
def root():
    return {
        "status": "online",
        "system": "SmartLab AI",
        "version": "1.0.0",
        "docs": "/docs",
    }


@app.get("/api/health")
def health_check():
    return {"status": "ok"}
