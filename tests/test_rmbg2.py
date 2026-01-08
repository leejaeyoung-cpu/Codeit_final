"""
RMBG-2.0 Background Removal Tests
"""
import pytest
from PIL import Image
import numpy as np
from app.core.background_removal_rmbg import BackgroundRemovalServiceRMBG


@pytest.fixture
def sample_image():
    """Create a sample RGB image for testing"""
    # Create a simple 512x512 RGB image
    img_array = np.random.randint(0, 255, (512, 512, 3), dtype=np.uint8)
    return Image.fromarray(img_array, mode='RGB')


@pytest.fixture
def rmbg_service():
    """Create RMBG-2.0 service instance"""
    return BackgroundRemovalServiceRMBG(device="cpu")  # Use CPU for testing


class TestRMBG2Initialization:
    """Test RMBG-2.0 service initialization"""
    
    def test_service_creation(self):
        """Test that service can be created"""
        service = BackgroundRemovalServiceRMBG(device="cpu")
        assert service is not None
        assert service.model_name == "briaai/RMBG-2.0"
    
    def test_device_selection_auto(self):
        """Test automatic device selection"""
        service = BackgroundRemovalServiceRMBG(device="auto")
        assert service.device in ["cuda", "cpu"]
    
    def test_get_model_info(self, rmbg_service):
        """Test model info retrieval"""
        info = rmbg_service.get_model_info()
        assert "model_name" in info
        assert "device" in info
        assert info["model_name"] == "briaai/RMBG-2.0"


class TestBackgroundRemoval:
    """Test background removal functionality"""
    
    @pytest.mark.asyncio
    async def test_basic_removal(self, rmbg_service, sample_image):
        """Test basic background removal"""
        result = await rmbg_service.remove_background(sample_image)
        
        # Check result properties
        assert result is not None
        assert isinstance(result, Image.Image)
        assert result.mode == 'RGBA'
        assert result.size == sample_image.size
    
    @pytest.mark.asyncio
    async def test_rgba_input(self, rmbg_service):
        """Test with RGBA input"""
        # Create RGBA image
        img_array = np.random.randint(0, 255, (256, 256, 4), dtype=np.uint8)
        rgba_image = Image.fromarray(img_array, mode='RGBA')
        
        result = await rmbg_service.remove_background(rgba_image)
        assert result.mode == 'RGBA'
    
    @pytest.mark.asyncio
    async def test_different_sizes(self, rmbg_service):
        """Test with different image sizes"""
        sizes = [(256, 256), (512, 512), (1024, 1024), (800, 600)]
        
        for size in sizes:
            img_array = np.random.randint(0, 255, (*size, 3), dtype=np.uint8)
            image = Image.fromarray(img_array, mode='RGB')
            
            result = await rmbg_service.remove_background(image)
            assert result.size == size


class TestBatchProcessing:
    """Test batch background removal"""
    
    @pytest.mark.asyncio
    async def test_batch_removal(self, rmbg_service):
        """Test batch processing"""
        # Create multiple sample images
        images = []
        for _ in range(3):
            img_array = np.random.randint(0, 255, (256, 256, 3), dtype=np.uint8)
            images.append(Image.fromarray(img_array, mode='RGB'))
        
        results = await rmbg_service.batch_remove_background(images)
        
        assert len(results) == len(images)
        for result in results:
            assert isinstance(result, Image.Image)
            assert result.mode == 'RGBA'


class TestPreprocessing:
    """Test image preprocessing"""
    
    def test_preprocess_rgb(self, rmbg_service, sample_image):
        """Test preprocessing RGB image"""
        tensor, orig_size = rmbg_service.preprocess_image(sample_image)
        
        assert tensor is not None
        assert tensor.shape[0] == 1  # Batch size
        assert tensor.shape[1] == 3  # RGB channels
        assert orig_size == sample_image.size
    
    def test_preprocess_grayscale(self, rmbg_service):
        """Test preprocessing grayscale image (should convert to RGB)"""
        # Create grayscale image
        img_array = np.random.randint(0, 255, (256, 256), dtype=np.uint8)
        gray_image = Image.fromarray(img_array, mode='L')
        
        tensor, orig_size = rmbg_service.preprocess_image(gray_image)
        assert tensor.shape[1] == 3  # Should be converted to RGB


class TestMaskPostprocessing:
    """Test mask postprocessing"""
    
    def test_postprocess_mask(self, rmbg_service):
        """Test mask postprocessing"""
        import torch
        
        # Create dummy mask tensor
        mask_tensor = torch.rand(1, 1, 1024, 1024)
        original_size = (512, 512)
        
        result = rmbg_service.postprocess_mask(mask_tensor, original_size)
        
        assert isinstance(result, Image.Image)
        assert result.mode == 'L'  # Grayscale alpha mask
        assert result.size == original_size


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
