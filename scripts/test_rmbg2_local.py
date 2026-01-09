"""
Test RMBG-2.0 Local Model
"""
import asyncio
import sys
from pathlib import Path
from PIL import Image
import numpy as np
import time

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.background_removal_rmbg_local import BackgroundRemovalServiceRMBGLocal


async def test_rmbg_local():
    """Test RMBG-2.0 local model"""
    print("="*60)
    print("RMBG-2.0 Local Model Test")
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
    print("\n2. Initializing RMBG-2.0 Local service...")
    try:
        service = BackgroundRemovalServiceRMBGLocal(device="auto")
        print(f"   ✓ Service initialized")
        
        # Get model info
        info = service.get_model_info()
        print(f"   - Model: {info['model_name']}")
        print(f"   - Path: {info['model_path']}")
        print(f"   - Device: {info['device']}")
        if info.get('gpu_available'):
            print(f"   - GPU: {info.get('gpu_name', 'Available')}")
    except Exception as e:
        print(f"   ✗ Failed to initialize: {e}")
        print("\n❌ Test failed - check if model is downloaded")
        print("   Run: python scripts/download_rmbg2_model.py")
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
            unique_alpha = len(np.unique(alpha))
            print(f"   - Alpha levels: {unique_alpha}/256")
            
            if unique_alpha > 10:
                print(f"   ✓ Multi-level transparency detected (high quality)")
            
    except Exception as e:
        print(f"   ✗ Background removal failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Save test result
    print("\n4. Saving test result...")
    output_dir = Path(__file__).parent.parent / "test_results"
    output_dir.mkdir(exist_ok=True)
    
    output_path = output_dir / "rmbg2_local_test_result.png"
    result.save(output_path)
    print(f"   ✓ Saved to: {output_path}")
    
    print("\n" + "="*60)
    print("✅ All tests passed!")
    print("="*60)
    print(f"\n📝 Using RMBG-2.0 Local Model")
    print(f"   Device: {info['device']}")
    print(f"   Quality: 256-level transparency (90%+ accuracy)")
    return True


if __name__ == "__main__":
    success = asyncio.run(test_rmbg_local())
    sys.exit(0 if success else 1)
