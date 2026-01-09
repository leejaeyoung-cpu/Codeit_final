"""
RMBG-2.0 Background Removal Service
Uses Hugging Face Inference API for briaai/RMBG-2.0 model
"""
from typing import List, Optional
from PIL import Image
import io
import os
import logging
from huggingface_hub import InferenceClient

logger = logging.getLogger(__name__)


class BackgroundRemovalServiceRMBG:
    """Service for AI-powered background removal using RMBG-2.0 via Inference API"""
    
    def __init__(self, device: str = "auto", api_key: Optional[str] = None):
        """
        Initialize the RMBG-2.0 background removal service using Hugging Face Inference API
        
        Args:
            device: Ignored for API-based inference (kept for compatibility)
            api_key: Hugging Face API token (will use HF_TOKEN env var if not provided)
        """
        logger.info("Initializing RMBG-2.0 background removal service (Inference API)")
        
        self.model_name = "briaai/RMBG-2.0"
        
        # Get API key from parameter or environment
        self.api_key = api_key or os.environ.get("HF_TOKEN")
        
        if not self.api_key:
            logger.warning("HF_TOKEN not found. RMBG-2.0 may require authentication.")
            logger.warning("Set HF_TOKEN environment variable or pass api_key parameter.")
        
        try:
            # Initialize Hugging Face Inference Client
            self.client = InferenceClient(
                provider="hf-inference",
                token=self.api_key,
            )
            logger.info("RMBG-2.0 Inference API client initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing RMBG-2.0 Inference API: {e}")
            raise
    
    async def remove_background(self, image: Image.Image) -> Image.Image:
        """
        Remove background from image using RMBG-2.0 Inference API
        
        Args:
            image: Input PIL Image (RGB)
            
        Returns:
            Image with background removed (RGBA with transparent background)
        """
        try:
            original_size = image.size
            logger.info(f"Processing image with RMBG-2.0 API: size={original_size}")
            
            # Convert to RGB if necessary
            if image.mode not in ['RGB', 'RGBA']:
                image = image.convert('RGB')
            
            # Save image to bytes
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format='PNG')
            img_byte_arr.seek(0)
            
            # Call Inference API
            try:
                # InferenceClient.image_segmentation returns the result image
                result = self.client.image_segmentation(
                    img_byte_arr.getvalue(),
                    model=self.model_name
                )
                
                # Result should be a PIL Image with transparent background
                if isinstance(result, Image.Image):
                    output_image = result
                else:
                    # If result is bytes, convert to PIL Image
                    output_image = Image.open(io.BytesIO(result))
                
                # Ensure RGBA mode
                if output_image.mode != 'RGBA':
                    output_image = output_image.convert('RGBA')
                
                # Resize to original size if different
                if output_image.size != original_size:
                    output_image = output_image.resize(original_size, Image.Resampling.LANCZOS)
                
                logger.info(f"Background removed successfully with RMBG-2.0 API")
                return output_image
                
            except Exception as api_error:
                logger.error(f"Inference API call failed: {api_error}")
                logger.error("This may be due to missing HF_TOKEN or model access restrictions")
                raise
            
        except Exception as e:
            logger.error(f"Error removing background with RMBG-2.0 API: {e}")
            raise
    
    async def batch_remove_background(self, images: List[Image.Image]) -> List[Image.Image]:
        """
        Remove background from multiple images
        
        Args:
            images: List of PIL Images
            
        Returns:
            List of images with backgrounds removed
        """
        results = []
        for idx, image in enumerate(images):
            try:
                result = await self.remove_background(image)
                results.append(result)
                logger.info(f"Processed image {idx + 1}/{len(images)}")
            except Exception as e:
                logger.error(f"Error processing image {idx + 1}: {e}")
                # Return original image on error
                results.append(image)
        
        return results
    
    def get_model_info(self) -> dict:
        """Get model information"""
        return {
            "model_name": self.model_name,
            "device": "api",  # Using Inference API
            "api_provider": "huggingface",
            "gpu_available": True,  # API uses GPU
            "has_token": bool(self.api_key)
        }
