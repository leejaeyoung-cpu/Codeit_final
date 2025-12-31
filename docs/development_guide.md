# AdGen_AI Image Processing - Development Guide

## 개발 환경 설정

### 1. 로컬 개발 환경

```bash
# 저장소 클론
git clone https://github.com/leejaeyoung-cpu/Codeit_final.git
cd Codeit_final

# 가상환경 생성 및 활성화
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# 의존성 설치
pip install -r requirements.txt

# 환경 변수 설정
copy .env.example .env
# .env 파일 편집
```

### 2. Docker 개발 환경

```bash
# Docker Compose로 전체 스택 실행
docker-compose up -d

# 로그 확인
docker-compose logs -f

# 특정 서비스만 재시작
docker-compose restart api
```

## 개발 워크플로우

### 브랜치 전략
- `main`: 프로덕션 브랜치
- `develop`: 개발 브랜치
- `feature/xxx`: 기능 개발
- `fix/xxx`: 버그 수정

### 코드 작성 규칙
- Python 스타일: PEP 8
- 포매터: Black
- 린터: Flake8
- 타입 체크: MyPy

```bash
# 코드 포맷팅
black app/

# 린팅
flake8 app/

# 타입 체크
mypy app/
```

## 테스트

```bash
# 전체 테스트 실행
pytest

# 특정 파일 테스트
pytest tests/test_background_removal.py

# 커버리지 리포트
pytest --cov=app --cov-report=html
```

## 디버깅

### VS Code 디버그 설정
`.vscode/launch.json`:
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "FastAPI",
      "type": "python",
      "request": "launch",
      "module": "uvicorn",
      "args": ["app.main:app", "--reload"],
      "jinja": true
    }
  ]
}
```

## 성능 프로파일링

```bash
# cProfile 사용
python -m cProfile -o output.prof scripts/benchmark.py

# 결과 확인
python -m pstats output.prof
```
