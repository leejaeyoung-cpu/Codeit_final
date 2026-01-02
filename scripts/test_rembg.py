"""
Simple Background Removal Test using rembg
Quick validation without Hugging Face authentication
"""
import asyncio
import time
from pathlib import Path
from PIL import Image
import sys
import os

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from rembg import remove
from app.core.image_processing import resize_to_instagram_ratio


async def test_with_rembg(image_path: str, output_dir: str = "test_results"):
    """
    Test background removal using rembg library
    
    Args:
        image_path: Path to input image
        output_dir: Directory to save results
    """
    print(f"\n{'='*60}")
    print(f"Testing Background Removal with rembg")
    print(f"{'='*60}\n")
    
    # Create output directory
    Path(output_dir).mkdir(exist_ok=True)
    
    # Load image
    print(f"📂 Loading image: {image_path}")
    try:
        input_image = Image.open(image_path)
        print(f"✅ Image loaded successfully")
        print(f"   Original size: {input_image.size}")
        print(f"   Mode: {input_image.mode}")
    except Exception as e:
        print(f"❌ Error loading image: {e}")
        return
    
    # Remove background
    print(f"\n🎨 Removing background...")
    start_process = time.time()
    try:
        output_image = remove(input_image)
        process_time = time.time() - start_process
        print(f"✅ Background removed in {process_time:.2f}s")
        print(f"   Result size: {output_image.size}")
        print(f"   Result mode: {output_image.mode}")
    except Exception as e:
        print(f"❌ Error removing background: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Save transparent version
    output_path = Path(output_dir) / "result_transparent.png"
    output_image.save(output_path, "PNG")
    print(f"\n💾 Saved transparent result: {output_path}")
    
    # Resize to Instagram 4:5 ratio
    print(f"\n📐 Resizing to Instagram 4:5 ratio (1080x1350)...")
    result_45 = resize_to_instagram_ratio(output_image, ratio="4:5")
    output_path_45 = Path(output_dir) / "result_instagram_4_5.png"
    result_45.save(output_path_45, "PNG")
    print(f"✅ Resized to {result_45.size}")
    print(f"💾 Saved Instagram 4:5 result: {output_path_45}")
    
    # Test with white background
    from app.core.image_processing import add_background_color
    result_white = add_background_color(result_45, background_color=(255, 255, 255))
    output_path_white = Path(output_dir) / "result_4_5_white_bg.jpg"
    result_white.save(output_path_white, "JPEG", quality=95)
    print(f"💾 Saved white background version: {output_path_white}")
    
    # Performance Summary
    print(f"\n{'='*60}")
    print(f"Performance Summary")
    print(f"{'='*60}")
    print(f"Background removal:   {process_time:.2f}s")
    print(f"\n✅ Target: < 5s for processing")
    if process_time < 5:
        print(f"✅ PASSED - Processing time meets target!")
    else:
        print(f"⚠️  WARNING - Processing time exceeds target")
    
    print(f"\n📊 Output Files:")
    print(f"   1. Transparent PNG: {output_path}")
    print(f"   2. Instagram 4:5 (transparent): {output_path_45}")
    print(f"   3. Instagram 4:5 (white bg): {output_path_white}")
    
    print(f"\n{'='*60}\n")


async def main():
    """Main function"""
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
    else:
        print("Usage: python test_rembg.py <image_path>")
        return
    
    await test_with_rembg(image_path)


if __name__ == "__main__":
    asyncio.run(main())
