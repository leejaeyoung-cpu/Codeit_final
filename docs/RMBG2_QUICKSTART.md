# RMBG-2.0 사용하기 (Hugging Face Inference API)

## 🚀 빠른 시작

RMBG-2.0은 이제 **Hugging Face Inference API**를 사용하므로 모델 다운로드가 **필요 없습니다**!

### 1️⃣ Hugging Face 토큰 얻기

1. **Hugging Face 계정 만들기**
   - https://huggingface.co/join

2. **RMBG-2.0 모델 액세스 요청**
   - https://huggingface.co/briaai/RMBG-2.0
   - "Accept license and access repository" 클릭

3. **액세스 토큰 생성**
   - https://huggingface.co/settings/tokens
   - "New token" 클릭
   - Name: `RMBG-2.0 API`
   - Type: `Read` 선택
   - "Generate token" 클릭
   - **토큰을 복사하세요!** (다시 볼 수 없습니다)

### 2️⃣ 토큰 설정

**`.env` 파일 생성** (프로젝트 루트 디렉토리):

```bash
# .env 파일
HF_TOKEN=hf_your_actual_token_here

# Background Removal 설정
BG_REMOVAL_MODEL=rmbg-2.0
BG_REMOVAL_FALLBACK=true
```

### 3️⃣ 서버 재시작

```bash
# 서버가 실행 중이면 중단 (Ctrl+C)
# 그 다음 재시작:
uvicorn app.main:app --reload
```

### 4️⃣ 테스트

```bash
# Health check (토큰 확인)
curl http://localhost:8000/api/v1/health

# 응답 예시:
# {
#   "model_name": "rmbg-2.0",
#   "device": "api",
#   "has_token": true  👈 이게 true여야 함!
# }
```

---

## ✨ 장점

### Inference API 사용 시
- ✅ **모델 다운로드 불필요** (~1.7GB 절약)
- ✅ **GPU 메모리 절약** (서버에서 실행)
- ✅ **빠른 시작** (설정만 하면 즉시 사용)
- ✅ **자동 업데이트** (모델 최신 버전 자동 사용)
- ⚠️ 인터넷 연결 필요
- ⚠️ API 호출 제한 있을 수 있음

### U2-Net (폴백) 사용 시
- ✅ **오프라인 작동**
- ✅ **API 제한 없음**
- ⚠️ 정확도 낮음 (25-37% vs 90%)

---

## 🔄 모델 전환

### RMBG-2.0 사용 (API)
```bash
# .env
HF_TOKEN=hf_your_token
BG_REMOVAL_MODEL=rmbg-2.0
```

### U2-Net 사용 (로컬)
```bash
# .env
BG_REMOVAL_MODEL=u2net
# HF_TOKEN 불필요
```

---

## 🐛 문제 해결

### "HF_TOKEN not found" 경고
- `.env` 파일에 `HF_TOKEN`이 설정되어 있는지 확인
- 파일 이름이 정확히 `.env`인지 확인 (`.env.example`이 아님)

### "Access denied" 또는 "401 Unauthorized"
- Hugging Face에서 RMBG-2.0 모델 액세스 승인 받았는지 확인
- 토큰이 `Read` 권한을 가지고 있는지 확인

### API 호출 실패
- 인터넷 연결 확인
- 일시적으로 U2-Net으로 전환: `BG_REMOVAL_MODEL=u2net`
- 서버 재시작

---

## 📚 추가 정보

- **Hugging Face Inference API 문서**: https://huggingface.co/docs/api-inference/
- **RMBG-2.0 모델 페이지**: https://huggingface.co/briaai/RMBG-2.0
- **토큰 관리**: https://huggingface.co/settings/tokens
