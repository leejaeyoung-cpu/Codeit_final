# 🚀 Background Removal Performance Benchmark Report

**Generated:** 2026-01-20 17:35:07

## Executive Summary

This report compares the performance of different background removal models on 5 test images.

## Models Tested

1. **U2-Net (rembg)**

## Performance Metrics

| Metric | U2-Net (rembg) |
|--------|--------|
| Success Rate | 5/5 (100.0%) |
| Avg Time | 2.616s |
| Median Time | 2.231s |
| Min Time | 2.087s |
| Max Time | 3.660s |
| Std Deviation | ±0.619s |

## 🎯 Recommendations

### Fastest Model
**U2-Net (rembg)** with average processing time of **2.616s**

### Quality vs Speed Trade-offs

- **U2-Net (rembg)**: Reliable, widely tested, good for general use
- **RMBG-2.0 (Local)**: Better edge detection, 256-level transparency, higher quality

## 📝 Notes

- All tests performed on the same hardware
- Processing times include preprocessing and postprocessing
- RMBG-2.0 provides superior edge quality with 256-level alpha masks
