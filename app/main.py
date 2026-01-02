"""
AdGen_AI Image Processing Module
Main FastAPI Application
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

app = FastAPI(
    title="AdGen_AI - Image Processing API",
    description="AI-powered background removal and image processing for fashion e-commerce",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create directories if they don't exist
UPLOAD_DIR = "uploads"
STATIC_DIR = "static"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(STATIC_DIR, exist_ok=True)

# Mount static files
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Include API routers
from app.api.v1 import image

app.include_router(image.router, prefix="/api/v1", tags=["Image Processing"])

@app.get("/")
async def root():
    """Serve the web UI"""
    index_path = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    else:
        return {
            "message": "AdGen_AI Image Processing API",
            "version": "1.0.0",
            "status": "active",
            "endpoints": {
                "ui": "/",
                "remove_background": "/api/v1/remove-background",
                "image_info": "/api/v1/image-info",
                "health": "/api/v1/health",
                "docs": "/docs"
            }
        }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

