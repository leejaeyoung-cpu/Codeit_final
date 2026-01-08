# RMBG-2.0 Integration Guide

## Overview

This guide covers the migration from rembg (U2-Net) to RMBG-2.0 for superior background removal quality.

## Performance Comparison

### RMBG-2.0 (New)
- ✅ **Accuracy**: 90.14% overall, 87-92% on complex backgrounds
- ✅ **Edge Quality**: 256-level transparency masks
- ✅ **Architecture**: BiRefNet (Bilateral Reference Network)
- ⚠️ **Memory**: 2-4GB GPU VRAM required
- ⚠️ **Speed**: ~3.5-4.5 seconds (slightly slower than U2-Net)

### U2-Net (Fallback)
- ✅ **Speed**: ~3.2 seconds
- ✅ **Memory**: ~1GB
- ⚠️ **Accuracy**: 25-37.5% on complex backgrounds
- ⚠️ **Edge Quality**: Binary masks only

**Result**: RMBG-2.0 provides **3x better accuracy** with superior edge quality at the cost of slightly higher processing time and memory usage.

---

## Installation

### 1. Install Dependencies

```bash
pip install huggingface-hub>=0.20.0 accelerate>=0.25.0
```

These are already included in `requirements.txt`.

### 2. Model Download

RMBG-2.0 model will be automatically downloaded from Hugging Face on first use:
- Model: `briaai/RMBG-2.0`
- Size: ~1.7GB
- Location: Default Hugging Face cache directory

**Note**: If you encounter access issues, the model may require authentication or may be temporarily unavailable. The system will automatically fall back to U2-Net.

---

## Configuration

### Environment Variables (.env)

```bash
# Background Removal Model Settings
BG_REMOVAL_MODEL=rmbg-2.0  # Options: rmbg-2.0, u2net
BG_REMOVAL_DEVICE=auto     # Options: cuda, cpu, auto
BG_REMOVAL_FALLBACK=true   # Enable automatic fallback to U2-Net
```

### Configuration Options

1. **`BG_REMOVAL_MODEL`**
   - `rmbg-2.0`: Use RMBG-2.0 model (recommended for quality)
   - `u2net`: Use U2-Net via rembg (faster, less memory)

2. **`BG_REMOVAL_DEVICE`**
   - `cuda`: Force GPU usage
   - `cpu`: Force CPU usage (slower but works everywhere)
   - `auto`: Automatically detect and use GPU if available

3. **`BG_REMOVAL_FALLBACK`**
   - `true`: Automatically fall back to U2-Net if RMBG-2.0 fails
   - `false`: Raise error if RMBG-2.0 fails

---

## Usage

### API Endpoint

The `/api/v1/remove-background` endpoint automatically uses the configured model:

```python
import requests

# Upload image
with open("product.jpg", "rb") as f:
    response = requests.post(
        "http://localhost:8000/api/v1/remove-background",
        files={"file": f},
        data={
            "ratio": "4:5",
            "style": "minimal"
        }
    )

# Check which model was used
model_used = response.headers.get("X-Model-Used")
print(f"Model used: {model_used}")  # "rmbg-2.0" or "u2net"

# Save result
with open("result.png", "wb") as f:
    f.write(response.content)
```

### Health Check

Check model status:

```bash
curl http://localhost:8000/api/v1/health
```

Response:
```json
{
  "status": "healthy",
  "model_name": "rmbg-2.0",
  "model_loaded": true,
  "device": "cuda",
  "gpu_available": true,
  "gpu_name": "NVIDIA GeForce RTX 3080",
  "styles_available": ["minimal", "mood", "street"]
}
```

---

## Testing

### Quick Test

```bash
python scripts/test_rmbg2_quick.py
```

This will:
1. Initialize RMBG-2.0 service
2. Process a test image
3. Save result to `test_results/`
4. Display timing and quality metrics

### Benchmark Comparison

Compare RMBG-2.0 vs U2-Net:

```bash
python scripts/benchmark_comparison.py
```

This will:
- Process 5 test images with both models
- Generate side-by-side comparisons
- Display performance statistics
- Save results to `test_results/benchmark_comparison/`

### Unit Tests

```bash
pytest tests/test_rmbg2.py -v
```

---

## Troubleshooting

### Issue: Model Download Fails

**Problem**: `Access to model briaai/RMBG-2.0 is restricted`

**Solutions**:
1. Check internet connection
2. Wait and retry (Hugging Face servers may be temporarily down)
3. Use U2-Net fallback by setting `BG_REMOVAL_MODEL=u2net`

### Issue: Out of Memory (OOM)

**Problem**: GPU runs out of memory

**Solutions**:
1. Reduce batch size in config
2. Process images sequentially
3. Use CPU mode: `BG_REMOVAL_DEVICE=cpu`
4. Fall back to U2-Net (uses less memory)

### Issue: Slow Processing on CPU

**Problem**: Processing takes >30 seconds per image

**Solutions**:
1. Use GPU if available: `BG_REMOVAL_DEVICE=cuda`
2. Switch to U2-Net for faster processing: `BG_REMOVAL_MODEL=u2net`
3. Reduce image size before processing

### Issue: Poor Quality Results

**Problem**: Background removal quality is not satisfactory

**Solutions**:
1. Ensure using RMBG-2.0: Check `X-Model-Used` header
2. Verify GPU is being used (faster and better quality)
3. Try different preprocessing styles
4. Check input image quality

---

## Rollback to U2-Net

If you need to revert to U2-Net:

1. Update `.env`:
   ```bash
   BG_REMOVAL_MODEL=u2net
   ```

2. Restart server:
   ```bash
   uvicorn app.main:app --reload
   ```

No code changes needed - the system automatically switches models.

---

## Performance Tips

### For Maximum Quality
```bash
BG_REMOVAL_MODEL=rmbg-2.0
BG_REMOVAL_DEVICE=cuda
```

### For Maximum Speed
```bash
BG_REMOVAL_MODEL=u2net
BG_REMOVAL_DEVICE=cuda
```

### For Low-Memory Environments
```bash
BG_REMOVAL_MODEL=u2net
BG_REMOVAL_DEVICE=cpu
```

---

## License

**IMPORTANT**: RMBG-2.0 is licensed under **CC BY-NC 4.0** (non-commercial use only).

- ✅ **Allowed**: Research, education, personal projects
- ❌ **Not Allowed**: Commercial use without license from BRIA AI
- 📝 **Commercial License**: Contact BRIA AI for commercial licensing

U2-Net (via rembg) has more permissive licensing suitable for commercial use.

---

## Additional Resources

- [RMBG-2.0 Model Card](https://huggingface.co/briaai/RMBG-2.0)
- [BiRefNet Paper](https://arxiv.org/abs/2401.17423)
- [BRIA AI Website](https://bria.ai/)
- [rembg GitHub](https://github.com/danielgatis/rembg)

---

## Support

For issues with:
- **RMBG-2.0 model**: Check Hugging Face model page
- **Integration**: Check this project's GitHub issues
- **Commercial licensing**: Contact BRIA AI directly
