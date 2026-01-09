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
from app.core.background_removal_rmbg import BackgroundRemovalServiceRMBG
from app.core.background_removal_rmbg_local import BackgroundRemovalServiceRMBGLocal
from app.core.image_processing import (
    resize_to_instagram_ratio,
    add_background_color,
    get_image_info
)
from app.core.style_processor import StyleProcessor
from app.core.storage import storage_service
from app.config import settings

logger = logging.getLogger(__name__)

router = APIRouter()

# Initialize services (singleton)
bg_removal_service = None
bg_removal_service_rmbg = None
bg_removal_service_rmbg_local = None
style_processor = None


def get_bg_removal_service():
    """
    Get or create background removal service instance
    
    Returns appropriate service based on configuration:
    - RMBG-2.0 (local) if use_local_model=True and model downloaded
    - RMBG-2.0 (API) if configured and HF_TOKEN available
    - Falls back to rembg (U2-Net) on error or if configured
    """
    global bg_removal_service, bg_removal_service_rmbg, bg_removal_service_rmbg_local
    
    # Check configuration
    if settings.bg_removal_model == "rmbg-2.0":
        # Try local model first if configured
        if settings.bg_removal_use_local_model:
            try:
                if bg_removal_service_rmbg_local is None:
                    logger.info("Initializing RMBG-2.0 Local BackgroundRemovalService...")
                    bg_removal_service_rmbg_local = BackgroundRemovalServiceRMBGLocal(
                        device=settings.bg_removal_device,
                        model_path=settings.bg_removal_local_model_path
                    )
                return bg_removal_service_rmbg_local, "rmbg-2.0-local"
            except Exception as e:
                logger.error(f"Failed to initialize RMBG-2.0 Local: {e}")
                if not settings.bg_removal_fallback:
                    raise
                logger.info("Trying RMBG-2.0 API...")
        
        # Try API model
        try:
            if bg_removal_service_rmbg is None:
                logger.info("Initializing RMBG-2.0 API BackgroundRemovalService...")
                bg_removal_service_rmbg = BackgroundRemovalServiceRMBG(
                    device=settings.bg_removal_device
                )
            return bg_removal_service_rmbg, "rmbg-2.0-api"
        except Exception as e:
            logger.error(f"Failed to initialize RMBG-2.0 API: {e}")
            if not settings.bg_removal_fallback:
                raise
            logger.info("Falling back to rembg (U2-Net)")
    
    # Use rembg as default or fallback
    if bg_removal_service is None:
        logger.info("Initializing rembg (U2-Net) BackgroundRemovalService...")
        bg_removal_service = BackgroundRemovalService()
    
    return bg_removal_service, "u2net"


def get_style_processor() -> StyleProcessor:
    """Get or create style processor instance"""
    global style_processor
    if style_processor is None:
        logger.info("Initializing StyleProcessor...")
        style_processor = StyleProcessor()
    return style_processor




# ...

@router.post("/remove-background")
async def remove_background(
    file: UploadFile = File(...),
    ratio: str = Form(default="4:5"),
    background_color: Optional[str] = Form(default=None),
    style: str = Form(default="minimal"),
    enhance_color: bool = Form(default=True),
    remove_wrinkles: bool = Form(default=False),
    response_format: str = Form(default="image")  # "image" or "json"
):
    """
    Remove background from uploaded image with advanced processing
    
    Args:
        file: Image file to process
        ratio: Instagram aspect ratio ("4:5", "1:1", "16:9")
        background_color: Optional hex color for background (e.g., "#FFFFFF")
        style: Processing style ("minimal", "mood", "street")
        enhance_color: Apply automatic color correction
        remove_wrinkles: Apply wrinkle smoothing
        response_format: Response format ("image" for blob, "json" for URL)
    
    Returns:
        Processed image blob or JSON with result_url
    """
    start_time = time.time()
    timing = {}
    
    try:
        # Read uploaded file
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        
        logger.info(f"Processing image: {file.filename}, size: {image.size}, mode: {image.mode}")
        logger.info(f"Options: ratio={ratio}, style={style}, response_format={response_format}")
        
        # Get services
        bg_service, model_name = get_bg_removal_service()
        logger.info(f"Using background removal model: {model_name}")
        
        # 1. Remove background
        step_start = time.time()
        try:
            result = await bg_service.remove_background(image)
        except Exception as e:
            if settings.bg_removal_fallback and model_name.startswith("rmbg-2.0"):
                logger.warning(f"RMBG-2.0 failed: {e}. Falling back to U2-Net.")
                # Fallback to U2-Net
                fallback_service = BackgroundRemovalService()
                result = await fallback_service.remove_background(image)
                model_name = "u2net (fallback)"
            else:
                raise
        timing['background_removal'] = time.time() - step_start
        
        # 2. Apply style processing
        step_start = time.time()
        processor = get_style_processor()
        result = processor.process_with_style(result, style=style)
        timing['style_processing'] = time.time() - step_start
        
        # 3. Resize to Instagram ratio
        step_start = time.time()
        result = resize_to_instagram_ratio(result, ratio=ratio)
        timing['resize'] = time.time() - step_start
        
        # 4. Add background color if specified
        if background_color:
            step_start = time.time()
            # Parse hex color
            bg_color = tuple(int(background_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
            result = add_background_color(result, background_color=bg_color)
            timing['background_color'] = time.time() - step_start
            output_format = "JPEG"
            content_type = "image/jpeg"
        else:
            output_format = "PNG"
            content_type = "image/png"
        
        # Convert to bytes
        step_start = time.time()
        output_buffer = io.BytesIO()
        result.save(output_buffer, format=output_format, quality=95)
        output_buffer.seek(0)
        file_data = output_buffer.getvalue()
        timing['encoding'] = time.time() - step_start
        
        processing_time = time.time() - start_time
        timing['total'] = processing_time
        
        logger.info(f"Processing completed in {processing_time:.2f}s")
        
        # Handle response based on format
        if response_format == "json":
            # Upload to storage (GCS or Local)
            result_url = await storage_service.upload_file(
                file_data, 
                f"processed_{file.filename}",
                content_type=content_type
            )
            
            return {
                "result_url": result_url,
                "processing_time": processing_time,
                "model_used": model_name,
                "timing": timing
            }
        else:
            # Return image blob (Legacy support)
            media_type = f"image/{output_format.lower()}"
            return Response(
                content=file_data,
                media_type=media_type,
                headers={
                    "X-Processing-Time": str(processing_time),
                    "X-Processing-Style": style,
                    "X-Model-Used": model_name,
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
        service, model_name = get_bg_removal_service()
        
        health_info = {
            "status": "healthy",
            "model_name": model_name,
            "model_loaded": True,
            "styles_available": ["minimal", "mood", "street"]
        }
        
        # Add GPU info if using RMBG-2.0
        if model_name == "rmbg-2.0" and hasattr(service, 'get_model_info'):
            model_info = service.get_model_info()
            health_info.update(model_info)
        
        return health_info
        
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }
