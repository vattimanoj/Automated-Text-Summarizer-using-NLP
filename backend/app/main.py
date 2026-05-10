from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager
from app.routers import auth, summarization, feedback, user
from app.database import engine, Base
import logging
import threading
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

# Training is now separate - use command: python train_model.py
# Backend starts immediately without any training checks

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    # Startup
    print("\n" + "=" * 50)
    print("AUTOMATED TEXT SUMMARIZER - BACKEND STARTING")
    print("=" * 50)
    
    # Download NLTK data
    try:
        import nltk
        logger.info("Downloading NLTK data...")
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)
        nltk.download('punkt_tab', quiet=True)
    except Exception as e:
        logger.error(f"Error downloading NLTK data: {e}")
        
    print("[OK] Backend ready immediately")
    print("[OK] Using existing trained model (if available)")
    print("[OK] To train model: python train_model.py")
    print("=" * 50)
    
    logger.info("Backend started - no automatic training")
    logger.info("Use 'python train_model.py' command to train model separately")
    
    # Backend is ready immediately - no training checks
    yield
    
    # Shutdown
    print("Server shutting down...")

app = FastAPI(
    title="Automated Text Summarizer API",
    description="AI-powered abstractive text summarization system with continuous learning",
    version="1.0.0",
    lifespan=lifespan
)

# CORS - allow_credentials=True for Bearer token (no cookies)
# In production, we allow the Render domains
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
        auth = request.headers.get("authorization") or request.headers.get("Authorization")
        logger.info("AUTH %s: %s", request.url.path, "OK" if auth else "MISSING")
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
# This is useful if deploying as a single service
try:
    from pathlib import Path
    # Adjusted path to look for frontend build relative to this file
    frontend_build = Path(__file__).resolve().parents[2] / "frontend" / "build"
    if frontend_build.exists():
        # Fallback: return index.html for any non-API path (SPA routing)
        @app.get("/{full_path:path}")
        async def serve_spa(full_path: str):
            # Don't override API routes or static files
            if full_path.startswith("api/") or full_path.startswith("static/"):
                return None # FastAPI will continue to search for other matches
            
            index_file = frontend_build / "index.html"
            if index_file.exists():
                return FileResponse(str(index_file))
            return {"message": "Automated Text Summarizer API", "version": "1.0.0", "status": "running"}
        
        # Mount the static assets from the React build
        static_build_dir = frontend_build / "static"
        if static_build_dir.exists():
            app.mount("/", StaticFiles(directory=str(frontend_build), html=True), name="frontend")
            
        logger.info(f"Frontend build found and will be served from: {frontend_build}")
except Exception as e:
    # Non-fatal: if pathlib or mounting fails, continue serving API only
    logger.error(f"Error serving frontend build: {e}")
    logger.debug("No frontend build served; running API only.")
