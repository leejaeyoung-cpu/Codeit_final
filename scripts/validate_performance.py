"""
Performance Validation Script
Tests RMBG-2.0 background removal with sample images
"""
import asyncio
import time
from pathlib import Path
from PIL import Image
import sys
import os

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.background_removal import BackgroundRemovalService
from app.core.image_processing import resize_to_instagram_ratio, get_image_info


async def test_background_removal(image_path: str, output_dir: str = "test_results"):
    """
    Test background removal on a single image
    
    Args:
        image_path: Path to input image
        output_dir: Directory to save results
    """
    print(f"\n{'='*60}")
    print(f"Testing RMBG-2.0 Background Removal")
    print(f"{'='*60}\n")
    
    # Create output directory
    Path(output_dir).mkdir(exist_ok=True)
    
    # Load image
    print(f"📂 Loading image: {image_path}")
    try:
        image = Image.open(image_path)
        print(f"✅ Image loaded successfully")
        print(f"   Original size: {image.size}")
        print(f"   Mode: {image.mode}")
    except Exception as e:
        print(f"❌ Error loading image: {e}")
        return
    
    # Initialize service
    print(f"\n🤖 Initializing RMBG-2.0 model...")
    start_init = time.time()
    try:
        service = BackgroundRemovalService()
        init_time = time.time() - start_init
        print(f"✅ Model initialized in {init_time:.2f}s")
        print(f"   Device: {service.device}")
    except Exception as e:
        print(f"❌ Error initializing model: {e}")
        return
    
    # Remove background
    print(f"\n🎨 Removing background...")
    start_process = time.time()
    try:
        result = await service.remove_background(image)
        process_time = time.time() - start_process
        print(f"✅ Background removed in {process_time:.2f}s")
        print(f"   Result size: {result.size}")
        print(f"   Result mode: {result.mode}")
    except Exception as e:
        print(f"❌ Error removing background: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Save transparent version
    output_path = Path(output_dir) / "result_transparent.png"
    result.save(output_path, "PNG")
    print(f"\n💾 Saved transparent result: {output_path}")
    
    # Resize to Instagram 4:5 ratio
    print(f"\n📐 Resizing to Instagram 4:5 ratio (1080x1350)...")
    result_45 = resize_to_instagram_ratio(result, ratio="4:5")
    output_path_45 = Path(output_dir) / "result_instagram_4_5.png"
    result_45.save(output_path_45, "PNG")
    print(f"✅ Resized to {result_45.size}")
    print(f"💾 Saved Instagram 4:5 result: {output_path_45}")
    
    # Performance Summary
    print(f"\n{'='*60}")
    print(f"Performance Summary")
    print(f"{'='*60}")
    print(f"Model initialization: {init_time:.2f}s")
    print(f"Background removal:   {process_time:.2f}s")
    print(f"Total time:           {init_time + process_time:.2f}s")
    print(f"\n✅ Target: < 5s for processing")
    if process_time < 5:
        print(f"✅ PASSED - Processing time meets target!")
    else:
        print(f"⚠️  WARNING - Processing time exceeds target")
    
    print(f"\n{'='*60}\n")


async def create_test_image():
    """Create a simple test image if no image is provided"""
    print("Creating test image...")
    
    # Create a colorful test pattern
    img = Image.new('RGB', (800, 600), color='white')
    pixels = img.load()
    
    # Draw colored squares
    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]
    for idx, color in enumerate(colors):
        x_start = 100 + (idx % 2) * 300
        y_start = 100 + (idx // 2) * 200
        
        for i in range(x_start, x_start + 200):
            for j in range(y_start, y_start + 200):
                if 0 <= i < img.width and 0 <= j < img.height:
                    pixels[i, j] = color
    
    test_path = "test_image.jpg"
    img.save(test_path, "JPEG")
    print(f"✅ Test image created: {test_path}")
    return test_path


async def main():
    """Main function"""
    import sys
    
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
    else:
        print("No image provided, creating test image...")
        image_path = await create_test_image()
    
    await test_background_removal(image_path)


if __name__ == "__main__":
    asyncio.run(main())
