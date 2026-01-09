"""
Storage Service
Handles file uploads to Google Cloud Storage or local filesystem
"""
import os
import uuid
import logging
from pathlib import Path
from datetime import datetime
from typing import Optional
from google.cloud import storage
from app.config import settings

logger = logging.getLogger(__name__)

class StorageService:
    def __init__(self):
        self.storage_type = settings.storage_type
        self.bucket_name = settings.gcs_bucket_name
        self.upload_dir = Path(settings.upload_dir)
        
        # Initialize GCS client if needed
        self.gcs_client = None
        if self.storage_type == "gcs":
            try:
                if settings.google_application_credentials:
                    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = settings.google_application_credentials
                self.gcs_client = storage.Client()
                logger.info(f"Initialized GCS client for bucket: {self.bucket_name}")
            except Exception as e:
                logger.error(f"Failed to initialize GCS client: {e}")
                logger.warning("Falling back to local storage")
                self.storage_type = "local"
        
        # Ensure local upload directory exists
        if self.storage_type == "local":
            self.upload_dir.mkdir(parents=True, exist_ok=True)
            logger.info(f"Initialized local storage at: {self.upload_dir}")

    async def upload_file(self, file_data: bytes, filename: str, content_type: str = "image/png") -> str:
        """
        Upload file to storage and return public URL
        """
        # Generate unique filename
        ext = Path(filename).suffix
        if not ext:
            ext = ".png" if content_type == "image/png" else ".jpg"
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = str(uuid.uuid4())[:8]
        safe_filename = f"{timestamp}_{unique_id}{ext}"
        
        if self.storage_type == "gcs" and self.gcs_client:
            return self._upload_to_gcs(file_data, safe_filename, content_type)
        else:
            return self._upload_to_local(file_data, safe_filename)

    def _upload_to_gcs(self, file_data: bytes, filename: str, content_type: str) -> str:
        """Upload to Google Cloud Storage"""
        try:
            bucket = self.gcs_client.bucket(self.bucket_name)
            blob = bucket.blob(filename)
            
            blob.upload_from_string(file_data, content_type=content_type)
            
            # Make public if needed (or use signed URL)
            # blob.make_public()
            
            return blob.public_url
        except Exception as e:
            logger.error(f"GCS upload failed: {e}")
            raise

    def _upload_to_local(self, file_data: bytes, filename: str) -> str:
        """Save to local filesystem"""
        try:
            file_path = self.upload_dir / filename
            with open(file_path, "wb") as f:
                f.write(file_data)
            
            # Return local URL (assuming static file serving is set up)
            # Note: In production, this should be the full domain URL
            return f"/static/uploads/{filename}"
        except Exception as e:
            logger.error(f"Local save failed: {e}")
            raise

# Global instance
storage_service = StorageService()
