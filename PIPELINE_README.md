# Pipeline Integration - README

## 개요

이 브랜치는 배경 제거 파이프라인 통합 작업을 포함합니다. U2-Net과 RMBG-2.0 모델을 모두 지원하는 유연한 아키텍처를 구현했습니다.

## 주요 변경사항

### 🏗️ 새로운 아키텍처

**Service Layer (`app/service/processing/`)**
- `base.py`: 인터페이스 및 데이터 타입 정의
- `models.py`: 모델 어댑터 (U2Net, RMBG2Local, RMBG2API)
- `factory.py`: 모델 팩토리 패턴 구현
- `pipeline.py`: 메인 처리 파이프라인
- `config.py`: 파이프라인 설정

### 🔌 API 통합

**새로운 엔드포인트:**
- `GET /api/v1/pipeline/status`: 파이프라인 상태 확인
- `GET /api/v1/pipeline/metrics`: 처리 메트릭
- `GET /api/v1/models`: 사용 가능한 모델 목록
- `POST /api/v1/models/test/{model_type}`: 특정 모델 테스트

기존 엔드포인트는 모두 하위 호환성 유지

### ⚙️ 설정

**새로운 환경 변수 (app/config.py):**
```python
pipeline_enabled = True  # 파이프라인 활성화
pipeline_default_model = "u2net"  # 기본 모델
pipeline_fallback_enabled = True  # Fallback 활성화
pipeline_fallback_chain = "rmbg-2.0-local,rmbg-2.0-api,u2net"  # Fallback 순서
pipeline_batch_size = 10  # 배치 크기
pipeline_timeout = 30.0  # 타임아웃 (초)
pipeline_max_retries = 2  # 최대 재시도 횟수
pipeline_collect_metrics = True  # 메트릭 수집
```

## 사용법

### 1. 기본 사용 (기존 API와 동일)

```bash
curl -X POST "http://localhost:8000/api/v1/remove-background" \
  -F "file=@image.jpg" \
  -F "ratio=4:5" \
  -F "response_format=json"
```

### 2. 파이프라인 상태 확인

```bash
curl http://localhost:8000/api/v1/pipeline/status
```

### 3. 모델 목록 조회

```bash
curl http://localhost:8000/api/v1/models
```

### 4. 특정 모델 테스트

```bash
curl -X POST "http://localhost:8000/api/v1/models/test/u2net" \
  -F "file=@image.jpg"
```

### 5. 메트릭 조회

```bash
curl http://localhost:8000/api/v1/pipeline/metrics
```

## 특징

### ✅ 유연한 모델 선택
- 환경변수로 기본 모델 선택 가능
- 런타임 모델 전환 가능

### 🔄 자동 Fallback
- 주 모델 실패 시 자동으로 fallback 모델 사용
- fallback 체인 설정 가능

### 📊 모니터링
- 처리 메트릭 자동  수집
- 모델 health check
- 성능 통계

### 🎯 배치 처리
- 여러 이미지 동시 처리
- 설정 가능한 배치 크기

### ⚡ 성능 최적화
- 재시도 로직
- 타임아웃 처리
- 비동기 처리

## 테스트

### 서버 시작
```bash
python -m uvicorn app.main:app --reload
```

### Health Check
```bash
curl http://localhost:8000/api/v1/health
```

### 파이프라인 테스트
```python
from app.service.processing import BackgroundRemovalPipeline
from PIL import Image

# 파이프라인 생성
pipeline = BackgroundRemovalPipeline()

# 이미지 처리
image = Image.open("test.jpg")
result = await pipeline.process(image)

print(f"Success: {result.success}")
print(f"Model used: {result.model_used}")
print(f"Processing time: {result.processing_time}s")
```

## 성능

**U2-Net 벤치마크 결과:**
- 평균 처리 시간: 2.62초
- 최소 시간: 2.09초
- 최대 시간: 3.66초
- 성공률: 100%

## 향후 작업

- [ ] RMBG-2.0 모델 문제 해결
- [ ] 추가 모델 통합 (예: SAM)
- [ ] 성능 최적화
- [ ] 더 상세한 테스트 작성

## 변경된 파일

### 새로운 파일
- `app/service/__init__.py`
- `app/service/processing/__init__.py`
- `app/service/processing/base.py`
- `app/service/processing/models.py`
- `app/service/processing/factory.py`
- `app/service/processing/pipeline.py`
- `app/service/processing/config.py`

### 수정된 파일
- `app/config.py`: 파이프라인 설정 추가
- `app/api/v1/image.py`: 파이프라인 통합, 새 엔드포인트 추가

## 롤백 방법

파이프라인을 비활성화하려면 설정에서:
```python
pipeline_enabled = False
```

기존 레거시 서비스가 자동으로 사용됩니다.
