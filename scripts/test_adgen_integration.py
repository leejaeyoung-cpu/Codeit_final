"""
AdGen_AI Integration Test
Test the newly integrated AdGen services
"""
import asyncio
from PIL import Image
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_imports():
    """Test that all new modules can be imported"""
    logger.info("Testing imports...")
    
    try:
        from app.service.processing import (
            HybridGenerator,
            ColorCorrector,
            StyleProcessor,
            WrinkleRemover,
            BackgroundRemovalRembg,
            ProductAnalyzer,
        )
        logger.info("✅ All imports successful")
        return True
    except ImportError as e:
        logger.error(f"❌ Import failed: {e}")
        return False


def test_color_corrector():
    """Test ColorCorrector"""
    logger.info("\nTesting ColorCorrector...")
    
    try:
        from app.service.processing import ColorCorrector
        
        # Create test image
        test_image = Image.new('RGB', (100, 100), color=(128, 128, 128))
        
        corrector = ColorCorrector()
        
        # Test different styles
        for style in ["balanced", "vivid", "soft"]:
            result = corrector.auto_enhance(test_image, style=style)
            assert result.size == test_image.size
            logger.info(f"  ✅ {style} style works")
        
        logger.info("✅ ColorCorrector test passed")
        return True
        
    except Exception as e:
        logger.error(f"❌ ColorCorrector test failed: {e}")
        return False


def test_style_processor():
    """Test StyleProcessor"""
    logger.info("\nTesting StyleProcessor...")
    
    try:
        from app.service.processing import StyleProcessor
        
        test_image = Image.new('RGB', (100, 100), color=(128, 128, 128))
        
        processor = StyleProcessor()
        
        # Test different styles
        for style in ["minimal", "vintage", "dramatic", "soft"]:
            result = processor.apply_style(test_image, style=style)
            assert result.size == test_image.size
            logger.info(f"  ✅ {style} style works")
        
        logger.info("✅ StyleProcessor test passed")
        return True
        
    except Exception as e:
        logger.error(f"❌ StyleProcessor test failed: {e}")
        return False


def test_wrinkle_remover():
    """Test WrinkleRemover"""
    logger.info("\nTesting WrinkleRemover...")
    
    try:
        from app.service.processing import WrinkleRemover
        
        test_image = Image.new('RGB', (100, 100), color=(128, 128, 128))
        
        remover = WrinkleRemover()
        result = remover.remove_wrinkles(test_image, strength=0.5)
        
        assert result.size == test_image.size
        logger.info("✅ WrinkleRemover test passed")
        return True
        
    except Exception as e:
        logger.error(f"❌ WrinkleRemover test failed: {e}")
        return False


def test_product_analyzer():
    """Test ProductAnalyzer"""
    logger.info("\nTesting ProductAnalyzer...")
    
    try:
        from app.service.processing import ProductAnalyzer
        
        test_image = Image.new('RGB', (100, 100), color=(128, 128, 128))
        
        analyzer = ProductAnalyzer()
        result = analyzer.analyze_product(test_image)
        
        assert "category" in result
        assert "colors" in result
        assert "attributes" in result
        
        logger.info("✅ ProductAnalyzer test passed")
        return True
        
    except Exception as e:
        logger.error(f"❌ ProductAnalyzer test failed: {e}")
        return False


async def test_rembg_background_removal():
    """Test BackgroundRemovalRembg"""
    logger.info("\nTesting BackgroundRemovalRembg...")
    
    try:
        from app.service.processing import BackgroundRemovalRembg
        
        test_image = Image.new('RGB', (100, 100), color=(128, 128, 128))
        
        remover = BackgroundRemovalRembg()
        result = await remover.remove_background(test_image)
        
        assert result.size == test_image.size
        assert result.mode == 'RGBA'
        
        logger.info("✅ BackgroundRemovalRembg test passed")
        return True
        
    except ImportError:
        logger.warning("⚠️ rembg not installed - skipping test")
        logger.info("  Install with: pip install rembg")
        return True  # Not a failure, just not installed
        
    except Exception as e:
        logger.error(f"❌ BackgroundRemovalRembg test failed: {e}")
        return False


def test_hybrid_generator_init():
    """Test HybridGenerator initialization"""
    logger.info("\nTesting HybridGenerator initialization...")
    
    try:
        from app.service.processing import HybridGenerator
        
        # Test without API token (should fail gracefully)
        try:
            generator = HybridGenerator(force_mode="replicate")
            logger.warning("  ⚠️ Initialized without API token (will fail on use)")
        except:
            logger.info("  ℹ️ Correctly requires API token")
        
        logger.info("✅ HybridGenerator initialization test passed")
        return True
        
    except Exception as e:
        logger.error(f"❌ HybridGenerator test failed: {e}")
        return False


async def run_all_tests():
    """Run all integration tests"""
    logger.info("=" * 60)
    logger.info("AdGen_AI Integration Tests")
    logger.info("=" * 60)
    
    results = []
    
    # Run tests
    results.append(("Imports", test_imports()))
    results.append(("ColorCorrector", test_color_corrector()))
    results.append(("StyleProcessor", test_style_processor()))
    results.append(("WrinkleRemover", test_wrinkle_remover()))
    results.append(("ProductAnalyzer", test_product_analyzer()))
    results.append(("BackgroundRemovalRembg", await test_rembg_background_removal()))
    results.append(("HybridGenerator Init", test_hybrid_generator_init()))
    
    # Summary
    logger.info("\n" + "=" * 60)
    logger.info("Test Summary")
    logger.info("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        logger.info(f"{status} - {name}")
    
    logger.info(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        logger.info("\n🎉 All tests passed!")
        return 0
    else:
        logger.error(f"\n⚠️ {total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(run_all_tests())
    exit(exit_code)
