@echo off
chcp 65001 >nul
echo.
echo [AdGen AI - Server Start]
echo.
echo.

:: 가상환경 활성화
echo [1/3] 가상환경 활성화 중...
if exist .venv\Scripts\activate.bat (
    call .venv\Scripts\activate.bat
    echo ✓ 가상환경 활성화 완료
) else (
    echo ✗ 가상환경을 찾을 수 없습니다. setup_env.bat를 먼저 실행하세요.
    pause
    exit /b 1
)

echo.
echo [2/3] 환경 변수 확인 중...
if not exist .env (
    echo ✗ .env 파일이 없습니다. .env.example을 복사하여 .env를 만드세요.
    pause
    exit /b 1
)
echo ✓ 환경 변수 파일 존재

echo.
echo [3/3] FastAPI 서버 시작 중...
echo 서버 주소: http://127.0.0.1:8000
echo Swagger UI: http://127.0.0.1:8000/docs
echo.
echo 서버를 중지하려면 Ctrl+C를 누르세요.
echo.

uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload

pause
