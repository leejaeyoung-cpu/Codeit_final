"""
Image Processing API Endpoints
Handles background removal and image processing requests
"""
from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from fastapi.responses import Response
from PIL import Image
import io
import time
import logging
from typing import Optional

from app.core.background_removal import BackgroundRemovalService
from app.core.image_processing import (
    resize_to_instagram_ratio,
    add_background_color,
    get_image_info
)

logger = logging.getLogger(__name__)

router = APIRouter()

# Initialize background removal service (singleton)
bg_removal_service = None


def get_bg_removal_service() -> BackgroundRemovalService:
    """Get or create background removal service instance"""
    global bg_removal_service
    if bg_removal_service is None:
        logger.info("Initializing BackgroundRemovalService...")
        bg_removal_service = BackgroundRemovalService()
    return bg_removal_service


@router.post("/remove-background")
async def remove_background(
    file: UploadFile = File(...),
    ratio: str = Form(default="4:5"),
    background_color: Optional[str] = Form(default=None)
):
    """
    Remove background from uploaded image
    
    Args:
        file: Image file to process
        ratio: Instagram aspect ratio ("4:5", "1:1", "16:9")
        background_color: Optional hex color for background (e.g., "#FFFFFF")
                         If not provided, returns transparent PNG
    
    Returns:
        Processed image with background removed
    """
    start_time = time.time()
    
    try:
        # Read uploaded file
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        
        logger.info(f"Processing image: {file.filename}, size: {image.size}, mode: {image.mode}")
        
        # Get background removal service
        service = get_bg_removal_service()
        
        # Remove background
        result = await service.remove_background(image)
        
        # Resize to Instagram ratio
        result = resize_to_instagram_ratio(result, ratio=ratio)
        
        # Add background color if specified
        if background_color:
            # Parse hex color
            bg_color = tuple(int(background_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
            result = add_background_color(result, background_color=bg_color)
            output_format = "JPEG"
        else:
            output_format = "PNG"
        
        # Convert to bytes
        output_buffer = io.BytesIO()
        result.save(output_buffer, format=output_format, quality=95)
        output_buffer.seek(0)
        
        processing_time = time.time() - start_time
        logger.info(f"Processing completed in {processing_time:.2f}s")
        
        # Return image response
        media_type = f"image/{output_format.lower()}"
        return Response(
            content=output_buffer.getvalue(),
            media_type=media_type,
            headers={
                "X-Processing-Time": str(processing_time),
                "X-Output-Format": output_format,
                "Content-Disposition": f'attachment; filename="processed_{file.filename}"'
            }
        )
        
    except Exception as e:
        logger.error(f"Error processing image: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")


@router.post("/image-info")
async def get_image_metadata(file: UploadFile = File(...)):
    """
    Get metadata about uploaded image
    
    Args:
        file: Image file
        
    Returns:
        Image metadata (size, dimensions, format, etc.)
    """
    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        
        info = get_image_info(image)
        info["filename"] = file.filename
        info["content_type"] = file.content_type
        
        return info
        
    except Exception as e:
        logger.error(f"Error getting image info: {e}")
        raise HTTPException(status_code=400, detail=f"Error reading image: {str(e)}")


@router.get("/health")
async def health_check():
    """Health check endpoint for image processing service"""
    try:
        service = get_bg_removal_service()
        return {
            "status": "healthy",
            "model_loaded": service.model is not None,
            "device": service.device
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }
