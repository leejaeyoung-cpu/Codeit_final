@echo off
chcp 65001 >nul
echo.
echo [RMBG-2.0 Model Download]
echo.
echo.

:: 가상환경 활성화
if exist .venv\Scripts\activate.bat (
    call .venv\Scripts\activate.bat
) else (
    echo ✗ 가상환경을 찾을 수 없습니다.
    pause
    exit /b 1
)

echo RMBG-2.0 모델을 다운로드합니다...
echo 모델 크기: 약 1.7GB
echo 이 작업은 인터넷 속도에 따라 시간이 걸릴 수 있습니다.
echo.

set /p confirm="다운로드를 시작하시겠습니까? (Y/N): "
if /i not "%confirm%"=="Y" (
    echo 취소되었습니다.
    pause
    exit /b 0
)

echo.
echo 다운로드 중...

:: 다운로드 스크립트 실행
if exist scripts\download_rmbg2_model.py (
    python scripts\download_rmbg2_model.py
    if errorlevel 1 (
        echo ✗ 다운로드 실패
        echo.
        echo 문제 해결:
        echo 1. 인터넷 연결 확인
        echo 2. Hugging Face 서버 상태 확인
        echo 3. .env 파일의 HF_TOKEN 확인 (필요한 경우)
        pause
        exit /b 1
    )
    echo.
    echo ✓ 모델 다운로드 완료!
) else (
    echo ✗ 다운로드 스크립트를 찾을 수 없습니다: scripts\download_rmbg2_model.py
    pause
    exit /b 1
)

echo.
echo 모델 위치: %USERPROFILE%\.cache\huggingface\hub
echo.

pause
