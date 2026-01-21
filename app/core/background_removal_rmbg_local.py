"""
RMBG-2.0 Background Removal Service (Local Model)
Uses locally downloaded briaai/RMBG-2.0 model
"""
from typing import List, Optional
from PIL import Image
import torch
import numpy as np
import logging
from transformers import AutoModelForImageSegmentation
from torchvision import transforms
import os
from pathlib import Path

logger = logging.getLogger(__name__)


class BackgroundRemovalServiceRMBGLocal:
    """Service for AI-powered background removal using locally downloaded RMBG-2.0"""
    
    def __init__(self, device: str = "auto", model_path: Optional[str] = None):
        """
        Initialize the RMBG-2.0 background removal service with local model
        
        Args:
            device: Device to use ("cuda", "cpu", or "auto")
            model_path: Path to local model (default: ./models/rmbg-2.0)
        """
        logger.info("Initializing RMBG-2.0 background removal service (Local Model)")
        
        # Determine device
        if device == "auto":
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
        else:
            self.device = device
            
        logger.info(f"Using device: {self.device}")
        
        # Set model path
        if model_path is None:
            model_path = os.path.join(os.getcwd(), "models", "rmbg-2.0")
        
        self.model_path = model_path
        self.model_name = "briaai/RMBG-2.0"
        
        # Load model
        try:
            logger.info(f"Loading RMBG-2.0 model...")
            
            # Load directly from HuggingFace (caching handled automatically)
            logger.info("Loading from HuggingFace Hub...")
            self.model = AutoModelForImageSegmentation.from_pretrained(
                self.model_name,
                trust_remote_code=True
            )
            logger.info("Model loaded from HuggingFace successfully")
            
            self.model.to(self.device)
            self.model.eval()
            
            logger.info(f"RMBG-2.0 model ready on device: {self.device}")
            
            # Define image transforms
            self.transform_image = transforms.Compose([
                transforms.Resize((1024, 1024)),
                transforms.ToTensor(),
                transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
            ])
            
        except Exception as e:
            logger.error(f"Error loading RMBG-2.0 model: {e}")
            raise
    
    def preprocess_image(self, image: Image.Image) -> tuple:
        """
        Preprocess image for RMBG-2.0 model
        
        Args:
            image: Input PIL Image (RGB)
            
        Returns:
            Preprocessed tensor and original size
        """
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        original_size = image.size
        
        # Apply transforms
        input_tensor = self.transform_image(image)
        input_batch = input_tensor.unsqueeze(0).to(self.device)
        
        return input_batch, original_size
    
    def postprocess_mask(self, mask: torch.Tensor, original_size: tuple) -> Image.Image:
        """
        Postprocess model output to create alpha mask
        
        Args:
            mask: Model output tensor
            original_size: Original image size (width, height)
            
        Returns:
            PIL Image (L mode) with alpha mask
        """
        # Convert to numpy
        mask_np = mask.squeeze().cpu().numpy()
        
        # Normalize to 0-255 (256 levels of transparency)
        mask_np = (mask_np * 255).astype(np.uint8)
        
        # Create PIL image
        mask_img = Image.fromarray(mask_np, mode='L')
        
        # Resize to original size
        mask_img = mask_img.resize(original_size, Image.Resampling.LANCZOS)
        
        return mask_img
    
    async def remove_background(self, image: Image.Image) -> Image.Image:
        """
        Remove background from image using local RMBG-2.0
        
        Args:
            image: Input PIL Image (RGB)
            
        Returns:
            Image with background removed (RGBA with transparent background)
        """
        try:
            original_size = image.size
            logger.info(f"Processing image with RMBG-2.0 (local): size={original_size}")
            
            # Preprocess
            input_batch, orig_size = self.preprocess_image(image)
            
            # Run inference
            with torch.no_grad():
                output = self.model(input_batch)[-1].sigmoid()
            
            # Postprocess mask
            mask = self.postprocess_mask(output, original_size)
            
            # Convert original to RGBA
            if image.mode != 'RGBA':
                image = image.convert('RGBA')
            
            # Apply mask
            result = image.copy()
            result.putalpha(mask)
            
            logger.info(f"Background removed successfully with RMBG-2.0 (local)")
            return result
            
        except Exception as e:
            logger.error(f"Error removing background with RMBG-2.0 (local): {e}")
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
            "model_path": self.model_path,
            "device": self.device,
            "gpu_available": torch.cuda.is_available(),
            "gpu_name": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
            "local_model": True
        }
