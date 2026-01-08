"""
Quick test for current background removal (U2-Net)
"""
import asyncio
import sys
from pathlib import Path
from PIL import Image
import numpy as np
import time

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.background_removal import BackgroundRemovalService


async def test_current_model():
    """Test current background removal service"""
    print("="*60)
    print("Background Removal Test (Current Model)")
    print("="*60)
    
    # Create test image
    print("\n1. Creating test image...")
    img_array = np.random.randint(100, 255, (800, 600, 3), dtype=np.uint8)
    # Add some structure
    img_array[:, :300, 0] = 220  # Red left half
    img_array[:, 300:, 2] = 220  # Blue right half
    test_image = Image.fromarray(img_array, mode='RGB')
    print(f"   ✓ Created {test_image.size} test image")
    
    # Initialize service
    print("\n2. Initializing background removal service...")
    try:
        service = BackgroundRemovalService()
        print(f"   ✓ Service initialized")
        print(f"   - Model: {service.model_name}")
    except Exception as e:
        print(f"   ✗ Failed to initialize: {e}")
        return False
    
    # Test background removal
    print("\n3. Testing background removal...")
    try:
        start = time.time()
        result = await service.remove_background(test_image)
        elapsed = time.time() - start
        
        print(f"   ✓ Background removed in {elapsed:.2f}s")
        print(f"   - Input:  {test_image.mode} {test_image.size}")
        print(f"   - Output: {result.mode} {result.size}")
        
        # Check alpha channel
        if result.mode == 'RGBA':
            alpha = np.array(result.split()[3])
            unique_values = len(np.unique(alpha))
            print(f"   - Alpha levels: {unique_values}")
            
    except Exception as e:
        print(f"   ✗ Background removal failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Save test result
    print("\n4. Saving test result...")
    output_dir = Path(__file__).parent.parent / "test_results"
    output_dir.mkdir(exist_ok=True)
    
    output_path = output_dir / "current_model_test_result.png"
    result.save(output_path)
    print(f"   ✓ Saved to: {output_path}")
    
    print("\n" + "="*60)
    print("✅ Test completed successfully!")
    print("="*60)
    print(f"\n📝 Note: Currently using {service.model_name}")
    print("   To use RMBG-2.0, the model needs to be downloaded first.")
    return True


if __name__ == "__main__":
    success = asyncio.run(test_current_model())
    sys.exit(0 if success else 1)
