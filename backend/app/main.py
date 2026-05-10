from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager
from app.routers import auth, summarization, feedback, user
from app.database import engine, Base
import logging
import sys
import os

# Configure logging to stdout for visibility
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# Create database tables
Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    # Startup
    print("\n" + "=" * 50)
    print("AUTOMATED TEXT SUMMARIZER - BACKEND STARTING")
    print("=" * 50)
    print("[OK] Backend ready immediately")
    print("[OK] Using existing trained model (if available)")
    print("[OK] To train model: python train_model.py")
    print("=" * 50)
    
    logger.info("Backend started - no automatic training")
    logger.info("Use 'python train_model.py' command to train model separately")
    
    yield
    
    # Shutdown
    print("Server shutting down...")

app = FastAPI(
    title="Automated Text Summarizer API",
    description="AI-powered abstractive text summarization system with continuous learning",
    version="1.0.0",
    lifespan=lifespan
)

# CORS configuration
allowed_origins = os.environ.get("ALLOWED_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if os.environ.get("ENV") != "production" else allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def log_auth_header(request, call_next):
    if request.url.path.startswith("/api/user") or request.url.path == "/api/auth/me":
        auth_header = request.headers.get("authorization") or request.headers.get("Authorization")
        logger.info("AUTH %s: %s", request.url.path, "OK" if auth_header else "MISSING")
    return await call_next(request)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(summarization.router, prefix="/api/summarize", tags=["Summarization"])
app.include_router(feedback.router, prefix="/api/feedback", tags=["Feedback"])
app.include_router(user.router, prefix="/api/user", tags=["User"])

# Mount static files directory for profile photos
if not os.path.exists("static"):
    os.makedirs("static", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    return {
        "message": "Automated Text Summarizer API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}

# If a production build of the frontend exists, serve it from the backend
try:
    from pathlib import Path
    frontend_build = Path(__file__).resolve().parents[2] / "frontend" / "build"
    if frontend_build.exists():
        @app.get("/{full_path:path}")
        async def serve_spa(full_path: str):
            if full_path.startswith("api/") or full_path.startswith("static/"):
                return None 
            
            index_file = frontend_build / "index.html"
            if index_file.exists():
                return FileResponse(str(index_file))
            return {"message": "Automated Text Summarizer API", "version": "1.0.0", "status": "running"}
        
        static_build_dir = frontend_build / "static"
        if static_build_dir.exists():
            app.mount("/", StaticFiles(directory=str(frontend_build), html=True), name="frontend")
            
        logger.info(f"Frontend build found and will be served from: {frontend_build}")
except Exception as e:
    logger.error(f"Error serving frontend build: {e}")
