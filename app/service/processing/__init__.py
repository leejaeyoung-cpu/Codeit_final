"""
Processing Pipeline Package
Background removal and image processing pipelines
"""
from app.service.processing.pipeline import BackgroundRemovalPipeline
from app.service.processing.factory import ModelFactory
from app.service.processing.base import (
    BackgroundRemovalProtocol,
    ProcessingResult,
    ModelType,
    ProcessingStatus,
)

__all__ = [
    "BackgroundRemovalPipeline",
    "ModelFactory",
    "BackgroundRemovalProtocol",
    "ProcessingResult",
    "ModelType",
    "ProcessingStatus",
]
