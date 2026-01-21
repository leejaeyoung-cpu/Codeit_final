# AdGen_AI Services Integration

## 🆕 새로 추가된 기능

팀 레포에 AdGen_AI의 processing 서비스가 통합되었습니다!

### 📦 통합된 모듈

#### 1. **Generators** (`app/service/processing/generators/`)
배경 자동 생성 기능

- **HybridGenerator**: GPU/Replicate API 자동 선택
  - 로컬 GPU 사용 가능 시 SDXL 로컬 실행
  - GPU 불가능 시 Replicate API로 자동 전환
  - Fallback 메커니즘 내장

```python
from app.service.processing import HybridGenerator

# 자동 모드 (GPU 자동 감지)
generator = HybridGenerator()

# 배경 생성
result = generator.generate_background(
    product_image=transparent_image,
    prompt_text="white minimal background",
    style="minimal",
    aspect_ratio="square"
)
```

#### 2. **Post Processors** (`app/service/processing/post_processors/`)
이미지 후처리 기능

- **ColorCorrector**: 색상 보정 및 개선
- **StyleProcessor**: 스타일 효과 적용
- **WrinkleRemover**: 주름 제거
- **BackgroundRemovalRembg**: rembg 기반 배경 제거

```python
from app.service.processing import ColorCorrector, StyleProcessor

# 색상 보정
corrector = ColorCorrector()
enhanced = corrector.auto_enhance(image, style="vivid")

# 스타일 적용
processor = StyleProcessor()
styled = processor.apply_style(image, style="minimal")
```

#### 3. **Vision** (`app/service/processing/vision/`)
제품 분석 기능

- **ProductAnalyzer**: AI 기반 제품 분석
- **VisionProviders**: Vision API 추상화

```python
from app.service.processing import ProductAnalyzer

analyzer = ProductAnalyzer()
analysis = analyzer.analyze_product(image)
# Returns: category, colors, attributes
```

---

## 🔧 환경 설정

### 새로운 의존성 설치

```bash
pip install replicate  # Replicate API (배경 생성용)
```

### 환경 변수

`.env` 파일에 추가:

```env
# Replicate API (배경 생성 사용 시)
REPLICATE_API_TOKEN=your_replicate_token_here
```

---

## 📖 사용 예시

### 전체 파이프라인 예제

```python
from app.service.processing import (
    BackgroundRemovalPipeline,
    HybridGenerator,
    ColorCorrector,
    StyleProcessor
)
from PIL import Image

# 1. 배경 제거
pipeline = BackgroundRemovalPipeline()
result = pipeline.process(original_image)
transparent = result.image

# 2. 색상 보정
corrector = ColorCorrector()
enhanced = corrector.auto_enhance(transparent, style="vivid")

# 3. 배경 생성
generator = HybridGenerator(replicate_api_token="your_token")
final = generator.generate_background(
    product_image=enhanced,
    prompt_text="minimalist white studio background",
    style="minimal"
)

# 4. 스타일 적용
processor = StyleProcessor()
styled = processor.apply_style(final, style="minimal")

styled.save("final_result.png")
```

---

## 🧪 테스트

```bash
# 기존 파이프라인 테스트 (회귀 테스트)
python -m pytest tests/test_pipeline.py

# 새 기능 테스트
python scripts/test_adgen_integration.py
```

---

## 📚 디렉토리 구조

```
app/service/processing/
├── __init__.py                  # 통합 export
├── base.py                      # 기본 타입 및 인터페이스
├── config.py                    # 파이프라인 설정
├── factory.py                   # 모델 팩토리
├── models.py                    # 모델 어댑터 (U2Net, RMBG-2.0)
├── pipeline.py                  # 배경 제거 파이프라인
├── generators/                  # 🆕 배경 생성
│   ├── __init__.py
│   ├── hybrid_generator.py
│   └── replicate_generator.py
├── post_processors/             # 🆕 후처리
│   ├── __init__.py
│   ├── background_removal_rembg.py
│   ├── color_correction.py
│   ├── style_processor.py
│   └── wrinkle_removal.py
└── vision/                      # 🆕 제품 분석
    ├── __init__.py
    ├── product_analyzer.py
    └── providers.py
```

---

## ⚠️ 주의사항

1. **메모리 요구사항**: SDXL 로컬 모드는 최소 6GB GPU 메모리 필요
2. **API 비용**: Replicate API는 종량제 (GPU 없을 시 자동 사용)
3. **호환성**: 기존 배경 제거 파이프라인은 그대로 유지됨

---

## 🔗 관련 링크

- [AdGen_AI 원본 레포](https://github.com/Dongjin-1203/AdGen_AI)
- [Replicate API 문서](https://replicate.com/docs)
