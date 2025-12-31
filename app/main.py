"""
AdGen_AI Image Processing Module
Main FastAPI Application
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "AdGen_AI Image Processing API",
        "version": "1.0.0",
        "status": "active"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

# TODO: Add API routers
# from app.api.v1 import image
# app.include_router(image.router, prefix="/api/v1")
