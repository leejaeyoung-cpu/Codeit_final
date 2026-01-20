"""
Comprehensive Performance Benchmark
Compares all available background removal models
"""
import asyncio
import time
import sys
from pathlib import Path
from PIL import Image
import numpy as np
from typing import List, Dict
import json
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.background_removal import BackgroundRemovalService
from app.core.background_removal_rmbg_local import BackgroundRemovalServiceRMBGLocal


def load_test_images(image_dir: Path = None) -> List[Image.Image]:
    """Load real test images if available, otherwise create synthetic ones"""
    images = []
    
    if image_dir and image_dir.exists():
        print(f"📂 Loading images from {image_dir}...")
        for ext in ['*.jpg', '*.jpeg', '*.png']:
            for img_path in sorted(image_dir.glob(ext)):
                try:
                    img = Image.open(img_path).convert('RGB')
                    # Resize if too large for faster testing
                    if max(img.size) > 1500:
                        img.thumbnail((1500, 1500))
                    images.append(img)
                    print(f"  ✓ {img_path.name} ({img.size[0]}x{img.size[1]})")
                except Exception as e:
                    print(f"  ✗ Failed to load {img_path}: {e}")
    
    if not images:
        print("⚠️  No real images found. Creating synthetic test images...")
        images = create_synthetic_images(num_images=5)
        
    return images


def create_synthetic_images(num_images: int = 5) -> List[Image.Image]:
    """Create synthetic test images for benchmarking"""
    images = []
    sizes = [(512, 512), (1024, 1024), (800, 600), (1200, 800), (640, 640)]
    
    print("🎨 Creating synthetic test images...")
    for i in range(num_images):
        size = sizes[i % len(sizes)]
        # Create colored image with patterns
        img_array = np.random.randint(100, 255, (*size, 3), dtype=np.uint8)
        # Add structure
        img_array[:, :size[1]//2, 0] = 200  # Red half
        img_array[:, size[1]//2:, 2] = 200  # Blue half
        
        images.append(Image.fromarray(img_array, mode='RGB'))
        print(f"  Created image {i+1}: {size[0]}x{size[1]}")
    
    return images


async def benchmark_model(service, images: List[Image.Image], model_name: str) -> Dict:
    """Benchmark a single model"""
    print(f"\n{'='*70}")
    print(f"🔬 Benchmarking: {model_name}")
    print(f"{'='*70}")
    
    times = []
    results = []
    memory_usage = []
    
    for idx, image in enumerate(images):
        print(f"\n  Image {idx+1}/{len(images)} - Size: {image.size[0]}x{image.size[1]}")
        
        start_time = time.time()
        try:
            result = await service.remove_background(image)
            process_time = time.time() - start_time
            times.append(process_time)
            results.append(result)
            
            # Analyze result quality
            alpha_info = ""
            if result.mode == 'RGBA':
                alpha = np.array(result.split()[3])
                unique_values = len(np.unique(alpha))
                alpha_info = f"Alpha levels: {unique_values}"
            
            print(f"    ✓ Time: {process_time:.3f}s | Output: {result.mode} | {alpha_info}")
            
        except Exception as e:
            print(f"    ✗ Error: {e}")
            times.append(None)
            results.append(None)
    
    # Calculate statistics
    valid_times = [t for t in times if t is not None]
    
    stats = {
        "model_name": model_name,
        "total_images": len(images),
        "successful": len(valid_times),
        "failed": len(images) - len(valid_times),
        "avg_time": float(np.mean(valid_times)) if valid_times else None,
        "min_time": float(np.min(valid_times)) if valid_times else None,
        "max_time": float(np.max(valid_times)) if valid_times else None,
        "std_time": float(np.std(valid_times)) if valid_times else None,
        "median_time": float(np.median(valid_times)) if valid_times else None,
        "times": times
    }
    
    return stats, results


def print_comparison_table(all_stats: List[Dict]):
    """Print detailed comparison table"""
    print(f"\n{'='*100}")
    print("📊 COMPREHENSIVE PERFORMANCE COMPARISON")
    print(f"{'='*100}\n")
    
    # Header
    headers = ["Metric", *[s["model_name"] for s in all_stats]]
    col_widths = [30] + [25] * len(all_stats)
    
    # Print header
    header_line = ""
    for header, width in zip(headers, col_widths):
        header_line += f"{header:<{width}}"
    print(header_line)
    print("-" * 100)
    
    # Metrics to compare
    metrics = [
        ("Success Rate (%)", lambda s: f"{s['successful']/s['total_images']*100:.1f}%"),
        ("Average Time (s)", lambda s: f"{s['avg_time']:.3f}" if s['avg_time'] else "N/A"),
        ("Median Time (s)", lambda s: f"{s['median_time']:.3f}" if s['median_time'] else "N/A"),
        ("Min Time (s)", lambda s: f"{s['min_time']:.3f}" if s['min_time'] else "N/A"),
        ("Max Time (s)", lambda s: f"{s['max_time']:.3f}" if s['max_time'] else "N/A"),
        ("Std Dev (s)", lambda s: f"{s['std_time']:.3f}" if s['std_time'] else "N/A"),
    ]
    
    for metric_name, metric_fn in metrics:
        row = f"{metric_name:<{col_widths[0]}}"
        for i, stats in enumerate(all_stats):
            value = metric_fn(stats)
            row += f"{value:<{col_widths[i+1]}}"
        print(row)
    
    print("\n" + "="*100)


def generate_performance_report(all_stats: List[Dict], output_path: Path):
    """Generate a detailed markdown performance report"""
    
    report = f"""# 🚀 Background Removal Performance Benchmark Report

**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Executive Summary

This report compares the performance of different background removal models on {all_stats[0]['total_images']} test images.

## Models Tested

"""
    
    for i, stats in enumerate(all_stats, 1):
        report += f"{i}. **{stats['model_name']}**\n"
    
    report += "\n## Performance Metrics\n\n"
    report += "| Metric | " + " | ".join([s['model_name'] for s in all_stats]) + " |\n"
    report += "|--------|" + "|".join(["--------" for _ in all_stats]) + "|\n"
    
    # Add metrics rows
    metrics = [
        ("Success Rate", lambda s: f"{s['successful']}/{s['total_images']} ({s['successful']/s['total_images']*100:.1f}%)"),
        ("Avg Time", lambda s: f"{s['avg_time']:.3f}s" if s['avg_time'] else "N/A"),
        ("Median Time", lambda s: f"{s['median_time']:.3f}s" if s['median_time'] else "N/A"),
        ("Min Time", lambda s: f"{s['min_time']:.3f}s" if s['min_time'] else "N/A"),
        ("Max Time", lambda s: f"{s['max_time']:.3f}s" if s['max_time'] else "N/A"),
        ("Std Deviation", lambda s: f"±{s['std_time']:.3f}s" if s['std_time'] else "N/A"),
    ]
    
    for metric_name, metric_fn in metrics:
        row = f"| {metric_name} | " + " | ".join([metric_fn(s) for s in all_stats]) + " |\n"
        report += row
    
    # Add recommendations
    report += "\n## 🎯 Recommendations\n\n"
    
    # Find best performer
    valid_stats = [s for s in all_stats if s['avg_time'] is not None]
    if valid_stats:
        fastest = min(valid_stats, key=lambda s: s['avg_time'])
        report += f"### Fastest Model\n**{fastest['model_name']}** with average processing time of **{fastest['avg_time']:.3f}s**\n\n"
    
    report += "### Quality vs Speed Trade-offs\n\n"
    report += "- **U2-Net (rembg)**: Reliable, widely tested, good for general use\n"
    report += "- **RMBG-2.0 (Local)**: Better edge detection, 256-level transparency, higher quality\n\n"
    
    report += "## 📝 Notes\n\n"
    report += "- All tests performed on the same hardware\n"
    report += "- Processing times include preprocessing and postprocessing\n"
    report += "- RMBG-2.0 provides superior edge quality with 256-level alpha masks\n"
    
    # Save report
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\n📄 Report saved to: {output_path}")


async def save_comparison_images(all_results: Dict[str, List], output_dir: Path):
    """Save visual comparison images"""
    output_dir.mkdir(exist_ok=True, parents=True)
    
    print(f"\n💾 Saving comparison images to: {output_dir}")
    
    model_names = list(all_results.keys())
    num_images = len(all_results[model_names[0]])
    
    for idx in range(num_images):
        # Save individual results
        for model_name, results in all_results.items():
            if results[idx]:
                safe_name = model_name.replace(" ", "_").replace("(", "").replace(")", "")
                results[idx].save(output_dir / f"result_{idx+1}_{safe_name}.png")
        
        # Create side-by-side comparison if we have results
        valid_results = [(name, results[idx]) for name, results in all_results.items() if results[idx]]
        
        if len(valid_results) >= 2:
            first_img = valid_results[0][1]
            width = first_img.size[0] * len(valid_results)
            height = first_img.size[1]
            comparison = Image.new('RGBA', (width, height), (255, 255, 255, 255))
            
            for i, (name, img) in enumerate(valid_results):
                comparison.paste(img, (first_img.size[0] * i, 0))
            
            comparison.save(output_dir / f"comparison_{idx+1}_all.png")
    
    print(f"  ✓ Saved comparison images")


async def main():
    """Main benchmark function"""
    print("="*100)
    print("🎯 COMPREHENSIVE BACKGROUND REMOVAL BENCHMARK")
    print("="*100)
    
    # Load test images
    print("\n📸 Preparing test images...")
    test_image_dir = Path(__file__).parent.parent / "test_images"
    test_images = load_test_images(test_image_dir)
    print(f"\n  Total images to process: {len(test_images)}")
    
    # Initialize all services
    services = []
    
    # 1. U2-Net (rembg)
    try:
        print("\n🔧 Loading U2-Net (rembg)...")
        u2net_service = BackgroundRemovalService()
        services.append(("U2-Net (rembg)", u2net_service))
        print("  ✓ U2-Net loaded")
    except Exception as e:
        print(f"  ✗ Failed to load U2-Net: {e}")
    
    # 2. RMBG-2.0 Local
    try:
        print("\n🔧 Loading RMBG-2.0 (Local Model)...")
        rmbg_local_service = BackgroundRemovalServiceRMBGLocal(device="auto")
        
        # Get model info
        if hasattr(rmbg_local_service, 'get_model_info'):
            info = rmbg_local_service.get_model_info()
            print(f"  ✓ RMBG-2.0 loaded")
            print(f"    - Device: {info.get('device', 'unknown')}")
            if info.get('gpu_available'):
                print(f"    - GPU: {info.get('gpu_name', 'Available')}")
        
        services.append(("RMBG-2.0 (Local)", rmbg_local_service))
    except Exception as e:
        print(f"  ✗ Failed to load RMBG-2.0 Local: {e}")
    
    if not services:
        print("\n❌ No services loaded. Cannot run benchmark.")
        return
    
    # Run benchmarks
    all_stats = []
    all_results = {}
    
    for model_name, service in services:
        stats, results = await benchmark_model(service, test_images, model_name)
        all_stats.append(stats)
        all_results[model_name] = results
    
    # Print comparison
    print_comparison_table(all_stats)
    
    # Save results
    output_dir = Path(__file__).parent.parent / "test_results" / "comprehensive_benchmark"
    output_dir.mkdir(exist_ok=True, parents=True)
    
    # Save statistics JSON
    stats_file = output_dir / "benchmark_stats.json"
    with open(stats_file, 'w') as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "models": all_stats
        }, f, indent=2)
    print(f"\n📊 Statistics saved to: {stats_file}")
    
    # Generate markdown report
    report_file = output_dir / "PERFORMANCE_REPORT.md"
    generate_performance_report(all_stats, report_file)
    
    # Save comparison images
    await save_comparison_images(all_results, output_dir)
    
    print("\n" + "="*100)
    print("✅ COMPREHENSIVE BENCHMARK COMPLETE!")
    print("="*100)


if __name__ == "__main__":
    asyncio.run(main())
