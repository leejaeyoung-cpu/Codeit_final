# 🎯 AdGen_AI 코드베이스 설명서

## 📋 프로젝트 개요

**AdGen_AI**는 소규모 패션 쇼핑몰을 위한 AI 기반 이미지 처리 시스템입니다. 사용자가 휴대폰으로 촬영한 상품 이미지의 배경을 자동으로 제거하고, 스타일별로 전처리하여 인스타그램 광고용 이미지를 생성합니다.

### 핵심 기능
- **AI 배경 제거**: RMBG-2.0 및 U2-Net을 활용한 고품질 배경 제거
- **스타일별 전처리**: Minimal, Mood, Street 3가지 스타일 지원
- **색감 보정**: 자동 화이트 밸런스, CLAHE 향상
- **의류 주름 제거**: Bilateral Filter를 활용한 스마트 스무딩
- **RESTful API**: FastAPI 기반의 고성능 API 서버

---

## 🏗️ 시스템 아키텍처

```
┌─────────────┐
│  클라이언트  │ (웹/모바일)
└──────┬──────┘
       │ HTTP/HTTPS
       ▼
┌─────────────────┐
│   FastAPI       │ (main.py)
│   API Server    │
└──────┬──────────┘
       │
       ├──► 배경 제거 (background_removal.py)
       │     └─ RMBG-2.0 / U2-Net
       │
       ├──► 색감 보정 (color_correction.py)
       │     └─ 화이트밸런스, CLAHE, 채도 조절
       │
       ├──► 주름 제거 (wrinkle_removal.py)
       │     └─ Bilateral Filter, Guided Filter
       │
       └──► 스타일 처리 (style_processor.py)
             ├─ Minimal (전문적, 깔끔)
             ├─ Mood (감성적, 빈티지)
             └─ Street (생동감, 비비드)
```

---

## 📁 프로젝트 구조

```
e:\Codit\highproject/
├── app/                          # 메인 애플리케이션
│   ├── main.py                   # FastAPI 진입점
│   ├── config.py                 # 설정 관리
│   │
│   ├── api/                      # API 라우터
│   │   └── v1/
│   │       └── image.py          # 이미지 처리 엔드포인트
│   │
│   └── core/                     # 핵심 비즈니스 로직
│       ├── background_removal.py         # 배경 제거 (rembg)
│       ├── background_removal_rmbg.py    # RMBG-2.0 API
│       ├── background_removal_rmbg_local.py  # RMBG-2.0 로컬
│       ├── color_correction.py           # 색감 보정
│       ├── wrinkle_removal.py            # 주름 제거
│       ├── style_processor.py            # 스타일 처리
│       ├── image_processing.py           # 이미지 유틸리티
│       └── storage.py                    # 저장소 관리
│
├── scripts/                      # 유틸리티 스크립트
│   ├── test_rmbg2_local.py      # RMBG-2.0 테스트
│   ├── benchmark_comparison.py   # 성능 벤치마크
│   └── validate_performance.py   # 성능 검증
│
├── tests/                        # 테스트 코드
│   ├── test_background_removal.py
│   └── test_rmbg2.py
│
├── static/                       # 정적 파일 (웹 UI)
├── uploads/                      # 업로드 파일
├── models/                       # AI 모델
│
├── Dockerfile                    # Docker 이미지 정의
├── docker-compose.yml            # 멀티 컨테이너 오케스트레이션
├── requirements.txt              # Python 패키지 의존성
│
├── .env                          # 환경 변수 (실제 설정)
├── .env.example                  # 환경 변수 예시
│
└── README.md                     # 프로젝트 문서
```

---

## 🔧 핵심 모듈 상세 설명

### 1. **main.py** - FastAPI 애플리케이션

**역할**: API 서버의 진입점으로, FastAPI 앱을 초기화하고 라우터를 등록합니다.

**주요 기능**:
- FastAPI 앱 생성 및 설정
- CORS 미들웨어 설정 (크로스 도메인 요청 허용)
- 정적 파일 서빙 (`/static` 경로)
- API 라우터 등록 (`/api/v1`)
- 헬스체크 엔드포인트 (`/health`)

**주요 코드**:
```python
app = FastAPI(
    title="AdGen_AI - Image Processing API",
    description="AI-powered background removal...",
    version="1.0.0"
)

# CORS 설정 - 모든 출처 허용
app.add_middleware(CORSMiddleware, allow_origins=["*"], ...)

# API 라우터 포함
app.include_router(image.router, prefix="/api/v1", tags=["Image Processing"])
```

**엔드포인트**:
- `GET /` - 웹 UI 또는 API 정보 반환
- `GET /health` - 서버 상태 확인

---

### 2. **config.py** - 설정 관리

**역할**: 환경 변수 및 애플리케이션 설정을 중앙 집중식으로 관리합니다.

**주요 설정 항목**:

| 설정 | 기본값 | 설명 |
|------|--------|------|
| `bg_removal_model` | `"rmbg-2.0"` | 배경 제거 모델 선택 (rmbg-2.0, u2net) |
| `bg_removal_device` | `"auto"` | 디바이스 (cuda, cpu, auto) |
| `bg_removal_fallback` | `True` | RMBG-2.0 실패 시 U2-Net으로 폴백 |
| `max_image_size` | `4096` | 최대 이미지 크기 |
| `default_ratio` | `"4:5"` | 기본 비율 (인스타그램) |
| `storage_type` | `"local"` | 저장소 타입 (local, gcs) |

**사용 예시**:
```python
from app.config import settings

model_name = settings.bg_removal_model
device = settings.bg_removal_device
```

---

### 3. **api/v1/image.py** - 이미지 처리 API

**역할**: 배경 제거 및 이미지 처리 요청을 처리하는 RESTful API 엔드포인트입니다.

**주요 엔드포인트**:

#### `POST /api/v1/remove-background`
이미지의 배경을 제거하고 스타일을 적용합니다.

**요청 파라미터**:
- `file`: 업로드할 이미지 파일 (multipart/form-data)
- `ratio`: 출력 비율 (4:5, 1:1, 16:9) - 선택
- `style`: 스타일 (minimal, mood, street) - 기본: minimal
- `enhance_color`: 색감 보정 활성화 - 기본: true
- `remove_wrinkles`: 주름 제거 활성화 - 기본: false
- `response_format`: 응답 형식 (image, json) - 기본: image

**처리 흐름**:
```python
1. 이미지 업로드 및 검증
2. 배경 제거 서비스 초기화 (RMBG-2.0 또는 U2-Net)
3. 배경 제거 실행
4. 색감 보정 (선택 사항)
5. 주름 제거 (선택 사항)
6. 스타일 처리 (minimal/mood/street)
7. 결과 이미지 반환 (PNG 또는 JSON)
```

**응답**:
- `image` 형식: PNG 이미지 (직접 다운로드 가능)
- `json` 형식: Base64 인코딩된 이미지 + 메타데이터

#### `POST /api/v1/image-info`
이미지 메타데이터 조회

**응답**:
```json
{
  "filename": "product.jpg",
  "size": 524288,
  "dimensions": {"width": 1024, "height": 1280},
  "format": "JPEG",
  "mode": "RGB"
}
```

#### `GET /api/v1/health`
서비스 상태 확인

**응답**:
```json
{
  "status": "healthy",
  "model": "RMBG-2.0",
  "device": "cuda",
  "version": "1.0.0"
}
```

---

### 4. **core/background_removal.py** - 배경 제거 (Rembg)

**역할**: `rembg` 라이브러리를 사용하여 U2-Net 기반 배경 제거를 수행합니다.

**특징**:
- Hugging Face 인증 불필요 (온라인 없이 작동)
- Alpha Matting으로 엣지 품질 향상
- 비동기 처리 지원
- 배치 처리 지원

**주요 메서드**:

#### `remove_background(image: Image.Image) -> Image.Image`
단일 이미지의 배경 제거

**알고리즘**:
```python
result = remove(
    image,
    alpha_matting=True,              # 엣지 품질 향상
    alpha_matting_foreground_threshold=240,
    alpha_matting_background_threshold=10,
    alpha_matting_erode_size=10,
    post_process_mask=True           # 마스크 후처리
)
```

#### `batch_remove_background(images: List[Image.Image]) -> List[Image.Image]`
여러 이미지를 순차적으로 처리

**에러 처리**:
- 개별 이미지 처리 실패 시 원본 이미지 반환
- 로깅을 통한 상세 에러 추적

---

### 5. **core/color_correction.py** - 색감 보정

**역할**: 이미지의 색상, 밝기, 대비, 채도 등을 자동으로 보정합니다.

**주요 알고리즘**:

#### **Auto White Balance** (Gray World 알고리즘)
색온도를 자동으로 보정하여 자연스러운 색감 복원

```python
# LAB 색공간에서 A/B 채널의 평균을 중앙(128)으로 이동
avg_a = np.average(result[:, :, 1])
avg_b = np.average(result[:, :, 2])
result[:, :, 1] -= (avg_a - 128) * (result[:, :, 0] / 255.0) * 1.1
result[:, :, 2] -= (avg_b - 128) * (result[:, :, 0] / 255.0) * 1.1
```

#### **CLAHE** (Contrast Limited Adaptive Histogram Equalization)
적응형 히스토그램 평활화로 디테일과 대비 향상

```python
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
l = clahe.apply(l)  # L 채널에만 적용 (LAB 색공간)
```

#### **채도 향상** (Saturation Enhancement)
HSV 색공간에서 채도(S) 채널 조절

```python
hsv[:, :, 1] = hsv[:, :, 1] * 1.2  # 20% 채도 증가
```

#### **색온도 조절** (Color Temperature)
따뜻한/차가운 느낌 조절

```python
# 따뜻하게 (+): Red/Yellow 증가, Blue 감소
# 차갑게 (-): Blue 증가, Red 감소
```

**주요 메서드**:

#### `auto_enhance(image: Image.Image, style: str) -> Image.Image`
스타일에 따른 자동 색감 보정

| 스타일 | 특징 | 적용 |
|-------|------|------|
| **balanced** | 균형잡힌 보정 | 화이트밸런스 + CLAHE + 채도 1.1x + 샤프닝 |
| **vivid** | 생생한 색감 | 화이트밸런스 + CLAHE + 채도 1.3x + 대비 증가 |
| **soft** | 부드러운 느낌 | 화이트밸런스 + 채도 1.05x + 밝기 증가 |

---

### 6. **core/wrinkle_removal.py** - 주름 제거

**역할**: 의류의 불필요한 주름을 제거하면서 질감은 유지합니다.

**알고리즘**:
- **Bilateral Filter**: 엣지를 보존하면서 스무딩
- **Guided Filter**: 디테일을 유지하면서 부드럽게

**주요 메서드**:

#### `remove_wrinkles(image: Image.Image, strength: str) -> Image.Image`
주름 제거 강도 조절

| 강도 | Bilateral Filter | Guided Filter | 용도 |
|------|-----------------|---------------|------|
| **light** | d=5, sigma=25/25 | r=3, eps=0.001 | 미세 주름만 제거 |
| **medium** | d=7, sigma=50/50 | r=4, eps=0.01 | 중간 정도 주름 제거 |
| **strong** | d=9, sigma=75/75 | r=5, eps=0.1 | 강한 주름 제거 |

**처리 과정**:
```python
1. Alpha 채널 분리 (RGBA인 경우)
2. Bilateral Filter 적용 (엣지 보존 스무딩)
3. Guided Filter 적용 (디테일 보존)
4. 원본과 블렌딩 (자연스러운 결과)
5. Alpha 채널 복원
```

---

### 7. **core/style_processor.py** - 스타일 처리

**역할**: 3가지 스타일(Minimal, Mood, Street)에 맞게 이미지를 전처리합니다.

**스타일별 특징**:

#### **Minimal Style** - 전문적이고 깔끔한 스타일
```
1. 색감 보정 (vivid) - 선명한 색감
2. 주름 제거 (light) - 디테일 유지
3. 대비 증가 (1.2x) - 또렷한 윤곽
4. 샤프닝 (1.5x) - 날카로운 엣지
5. 드롭 섀도우 추가 - 전문적인 느낌
```

**사용 사례**: 제품 상세 페이지, 공식 광고

#### **Mood Style** - 감성적이고 빈티지한 스타일
```
1. 색감 보정 (soft) - 부드러운 색감
2. 주름 제거 (medium) - 자연스러운 스무딩
3. 따뜻한 색온도 (+30) - 따뜻한 느낌
4. 세피아 톤 (30%) - 빈티지 효과
5. 비네팅 효과 - 중앙 집중
6. 채도 감소 (0.9x) - 차분한 느낌
```

**사용 사례**: 인스타그램 감성 피드, 브랜드 스토리텔링

#### **Street Style** - 생동감 있고 비비드한 스타일
```
1. 색감 보정 (vivid) - 강렬한 색감
2. 주름 제거 (light) - 질감 유지
3. 채도 증가 (1.4x) - 비비드한 색상
4. 대비 증가 (1.3x) - 강한 대비
5. 샤프닝 (2.0x) - 날카로운 엣지
6. 차가운 색온도 (-10) - 쿨톤 도시 느낌
```

**사용 사례**: 스트릿 패션, 트렌디한 광고

**주요 메서드**:

#### `add_drop_shadow(image, offset, blur_radius) -> Image`
전문적인 드롭 섀도우 추가

#### `add_vignette(image, strength) -> Image`
중앙 집중 효과를 위한 비네팅

#### `process_with_style(image, style) -> Image`
선택한 스타일 자동 적용

---

## 🐳 Docker 환경

### **Dockerfile**

Python 3.10 기반 이미지로 애플리케이션 컨테이너화

**주요 단계**:
```dockerfile
1. Python 3.10-slim-bullseye 베이스 이미지
2. 시스템 패키지 설치 (OpenCV 의존성)
3. Python 패키지 설치 (requirements.txt)
4. 애플리케이션 코드 복사
5. 디렉토리 생성 (static/uploads, models)
6. 포트 노출 (8000)
7. Uvicorn 서버 실행
```

### **docker-compose.yml**

멀티 컨테이너 오케스트레이션

**서비스 구성**:

| 서비스 | 이미지 | 포트 | 역할 |
|--------|--------|------|------|
| **api** | Custom (Dockerfile) | 8000 | FastAPI 서버 |
| **worker** | Custom (Dockerfile) | - | Celery 워커 (비동기 작업) |
| **db** | postgres:15-alpine | 5432 | PostgreSQL 데이터베이스 |
| **redis** | redis:7-alpine | 6379 | Redis 캐시/메시지 브로커 |

**실행 방법**:
```bash
# 전체 스택 시작
docker-compose up -d

# 로그 확인
docker-compose logs -f api

# 중지
docker-compose down
```

---

## 📦 주요 의존성 (requirements.txt)

### **웹 프레임워크**
- `fastapi==0.104.1` - 고성능 웹 프레임워크
- `uvicorn[standard]==0.24.0` - ASGI 서버

### **이미지 처리**
- `rembg>=2.0.0` - U2-Net 배경 제거
- `Pillow==10.1.0` - 이미지 조작
- `opencv-python==4.8.1.78` - 컴퓨터 비전
- `numpy==1.24.3` - 배열 연산

### **딥러닝 (RMBG-2.0)**
- `torch==2.1.2` - PyTorch
- `transformers==4.36.2` - Hugging Face 모델
- `timm>=1.0.0` - BiRefNet 아키텍처
- `kornia==0.7.1` - 미분 가능한 이미지 처리

### **비동기 처리**
- `celery==5.3.4` - 분산 태스크 큐
- `redis==5.0.1` - 메시지 브로커/캐시

### **데이터베이스**
- `sqlalchemy==2.0.23` - ORM
- `psycopg2-binary==2.9.9` - PostgreSQL 드라이버

### **클라우드 스토리지**
- `google-cloud-storage==2.10.0` - GCS 연동

---

## 🔄 API 사용 예시

### **1. 배경 제거 (Minimal 스타일)**
```python
import requests

url = "http://localhost:8000/api/v1/remove-background"
files = {"file": open("product.jpg", "rb")}
data = {
    "style": "minimal",
    "enhance_color": True,
    "remove_wrinkles": False,
    "response_format": "image"
}

response = requests.post(url, files=files, data=data)

# 이미지 저장
with open("result.png", "wb") as f:
    f.write(response.content)
```

### **2. Mood 스타일 + 주름 제거**
```python
data = {
    "style": "mood",
    "enhance_color": True,
    "remove_wrinkles": True,
    "response_format": "json"
}

response = requests.post(url, files=files, data=data)
result = response.json()

# Base64 디코딩
import base64
image_data = base64.b64decode(result["image"])
with open("mood_result.png", "wb") as f:
    f.write(image_data)
```

### **3. Street 스타일 (4:5 비율)**
```python
data = {
    "ratio": "4:5",
    "style": "street",
    "enhance_color": True,
    "remove_wrinkles": False
}

response = requests.post(url, files=files, data=data)
```

---

## ⚡ 성능 최적화

### **1. 모델 선택**
- **RMBG-2.0**: 정확도 우선 (90%+) - GPU 권장
- **U2-Net**: 속도 우선 (~3초) - CPU 가능

### **2. 디바이스 설정**
```bash
# .env 파일
BG_REMOVAL_DEVICE=cuda    # GPU 사용
BG_REMOVAL_DEVICE=cpu     # CPU 사용
BG_REMOVAL_DEVICE=auto    # 자동 탐지
```

### **3. 배치 처리**
여러 이미지를 한 번에 처리하여 오버헤드 감소

### **4. Redis 캐싱**
자주 처리되는 이미지는 캐시에서 즉시 반환

---

## 🛠️ 트러블슈팅

### **문제 1: RMBG-2.0 로딩 실패**
**원인**: Hugging Face 인증 필요 또는 네트워크 문제

**해결책**:
```bash
# U2-Net으로 폴백 (자동)
BG_REMOVAL_FALLBACK=true

# 또는 직접 U2-Net 사용
BG_REMOVAL_MODEL=u2net
```

### **문제 2: 메모리 부족**
**원인**: RMBG-2.0이 GPU 메모리 2-4GB 필요

**해결책**:
```bash
# CPU 모드로 전환
BG_REMOVAL_DEVICE=cpu

# 또는 U2-Net 사용 (메모리 사용량 낮음)
BG_REMOVAL_MODEL=u2net
```

### **문제 3: 처리 시간 지연**
**원인**: CPU 모드 또는 큰 이미지

**해결책**:
- GPU 사용 (`BG_REMOVAL_DEVICE=cuda`)
- 이미지 크기 제한 (`max_image_size=2048`)
- U2-Net 사용 (더 빠름)

---

## 🎯 주요 기술 포인트

### **1. AI 모델 통합**
- **RMBG-2.0**: BiRefNet 아키텍처 기반 최신 모델
- **U2-Net**: 검증된 배경 제거 모델
- **Fallback 메커니즘**: 자동 모델 전환

### **2. 이미지 처리 파이프라인**
```
입력 → 배경 제거 → 색감 보정 → 주름 제거 → 스타일 처리 → 출력
```

### **3. 스타일별 전처리**
각 스타일(Minimal, Mood, Street)에 최적화된 알고리즘 조합

### **4. 비동기 처리**
- FastAPI의 비동기 엔드포인트
- Celery를 통한 백그라운드 작업

### **5. 마이크로서비스 아키텍처**
- API 서버, Worker, Database, Cache 분리
- Docker Compose로 오케스트레이션

---

## 📚 참고 자료

### **모델 및 논문**
- [RMBG-2.0 (Hugging Face)](https://huggingface.co/briaai/RMBG-2.0)
- [BiRefNet Paper](https://arxiv.org/abs/2401.17423)
- [U²-Net Paper](https://arxiv.org/abs/2005.09007)

### **라이브러리**
- [FastAPI 공식 문서](https://fastapi.tiangolo.com/)
- [rembg GitHub](https://github.com/danielgatis/rembg)
- [OpenCV 문서](https://docs.opencv.org/)
- [Pillow 문서](https://pillow.readthedocs.io/)

---

## 🎓 학습 포인트

### **Backend 개발**
- FastAPI를 활용한 RESTful API 설계
- 비동기 처리 (async/await)
- 환경 설정 관리 (pydantic-settings)

### **AI/ML 통합**
- Hugging Face 모델 통합
- PyTorch 모델 추론
- GPU/CPU 자동 감지

### **이미지 처리**
- OpenCV 고급 기법 (CLAHE, Bilateral Filter)
- PIL을 활용한 이미지 조작
- 색공간 변환 (RGB, LAB, HSV)

### **DevOps**
- Docker 컨테이너화
- Docker Compose 멀티 컨테이너
- 환경 변수 관리

### **코드 품질**
- 타입 힌팅 (Python Type Hints)
- 로깅 시스템
- 에러 핸들링

---

## 🚀 확장 가능성

### **단기 개선**
- [ ] 배치 처리 API 구현
- [ ] Redis 캐싱 시스템
- [ ] Google Cloud Storage 연동
- [ ] 성능 모니터링 (Prometheus)

### **장기 발전**
- [ ] 커스텀 배경 생성 (Stable Diffusion)
- [ ] 실시간 스트리밍 처리
- [ ] 모바일 앱 연동
- [ ] A/B 테스트 시스템

---

## 📞 개발자 정보

**이재영** - 이미지 처리 모듈 개발자
- GitHub: [@leejaeyoung-cpu](https://github.com/leejaeyoung-cpu)
- 프로젝트: [Codeit_final](https://github.com/leejaeyoung-cpu/Codeit_final)

---

**마지막 업데이트**: 2026-01-16  
**버전**: 1.0.0  
**라이선스**: MIT

---

> 이 문서는 AdGen_AI 프로젝트의 코드베이스를 종합적으로 설명합니다. 각 모듈의 역할, 구현 방법, 사용 예시를 통해 프로젝트의 전체 구조를 이해할 수 있습니다.
