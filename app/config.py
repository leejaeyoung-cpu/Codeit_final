"""
Application Configuration
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings"""
    
    # API Settings
    app_name: str = "AdGen AI - Background Removal"
    version: str = "1.0.0"
    debug: bool = False
    
    # Background Removal Model Settings
    bg_removal_model: str = "rmbg-2.0"  # Options: "rmbg-2.0", "u2net"
    bg_removal_device: str = "auto"  # Options: "cuda", "cpu", "auto"
    bg_removal_fallback: bool = True  # Enable fallback to u2net if rmbg-2.0 fails
    bg_removal_use_local_model: bool = False  # True: local model, False: Inference API
    bg_removal_local_model_path: Optional[str] = None  # Path to local model (None = ./models/rmbg-2.0)
    
    # Model Cache Settings
    model_cache_dir: Optional[str] = None  # None = use Hugging Face default cache
    
    # Processing Settings
    max_image_size: int = 4096  # Maximum image dimension
    default_ratio: str = "4:5"  # Default Instagram ratio
    
    # Performance Settings
    gpu_memory_fraction: float = 0.8  # Max GPU memory to use
    enable_half_precision: bool = False  # FP16 for faster processing (experimental)

    # Storage Settings
    storage_type: str = "local"  # "gcs" or "local"
    gcs_bucket_name: str = "adgen-ai-images"
    google_application_credentials: Optional[str] = None
    upload_dir: str = "static/uploads"  # For local storage
    
    class Config:
        # env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
