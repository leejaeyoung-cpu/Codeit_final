"""
Background Removal Tests
"""
import pytest
from PIL import Image
import numpy as np
import io
import asyncio

from app.core.background_removal import BackgroundRemovalService


@pytest.fixture
def sample_image():
    """Create a sample test image"""
    # Create a simple test image (red square on white background)
    img = Image.new('RGB', (400, 400), color='white')
    pixels = img.load()
    
    # Draw a red square in the center
    for i in range(100, 300):
        for j in range(100, 300):
            pixels[i, j] = (255, 0, 0)
    
    return img


@pytest.fixture
def bg_service():
    """Create background removal service instance"""
    return BackgroundRemovalService()


@pytest.mark.asyncio
async def test_model_initialization(bg_service):
    """Test that RMBG-2.0 model loads successfully"""
    assert bg_service.model is not None
    assert bg_service.device in ['cuda', 'cpu']
    assert bg_service.model_input_size == (1024, 1024)


@pytest.mark.asyncio
async def test_remove_background_basic(bg_service, sample_image):
    """Test basic background removal"""
    result = await bg_service.remove_background(sample_image)
    
    # Check that result is RGBA
    assert result.mode == 'RGBA'
    
    # Check size is preserved
    assert result.size == sample_image.size


@pytest.mark.asyncio
async def test_remove_background_different_modes(bg_service):
    """Test background removal with different image modes"""
    # Test with RGBA input
    rgba_img = Image.new('RGBA', (200, 200), color=(255, 255, 255, 255))
    result = await bg_service.remove_background(rgba_img)
    assert result.mode == 'RGBA'
    
    # Test with grayscale input
    gray_img = Image.new('L', (200, 200), color=128)
    result = await bg_service.remove_background(gray_img)
    assert result.mode == 'RGBA'


@pytest.mark.asyncio
async def test_batch_processing(bg_service, sample_image):
    """Test batch background removal"""
    # Create multiple test images
    images = [sample_image.copy() for _ in range(3)]
    
    results = await bg_service.batch_remove_background(images)
    
    assert len(results) == 3
    for result in results:
        assert result.mode == 'RGBA'


def test_processing_time(bg_service, sample_image, benchmark):
    """Benchmark processing time"""
    async def process():
        return await bg_service.remove_background(sample_image)
    
    # Run and time the operation
    result = asyncio.run(process())
    
    # Note: Actual benchmark would measure time
    # This is a placeholder for performance testing
    assert result is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
