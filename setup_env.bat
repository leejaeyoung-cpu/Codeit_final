@echo off
chcp 65001 >nul
echo.
echo [AdGen AI - Environment Setup]
echo.
echo.

:: Python 버전 확인
echo [1/5] Python 버전 확인 중...
python --version
if errorlevel 1 (
    echo ✗ Python이 설치되어 있지 않습니다.
    pause
    exit /b 1
)
echo ✓ Python 설치 확인 완료
echo.

:: 가상환경 생성
echo [2/5] 가상환경 생성 중...
if exist .venv (
    echo ! 가상환경이 이미 존재합니다. 건너뜁니다.
) else (
    python -m venv .venv
    echo ✓ 가상환경 생성 완료
)
echo.

:: 가상환경 활성화
echo [3/5] 가상환경 활성화 중...
call .venv\Scripts\activate.bat
echo ✓ 가상환경 활성화 완료
echo.

:: pip 업그레이드
echo [4/5] pip 업그레이드 중...
python -m pip install --upgrade pip
echo ✓ pip 업그레이드 완료
echo.

:: 의존성 설치
echo [5/5] 패키지 설치 중...
echo 이 작업은 몇 분 정도 걸릴 수 있습니다...
pip install -r requirements.txt
if errorlevel 1 (
    echo ✗ 패키지 설치 실패
    pause
    exit /b 1
)
echo ✓ 패키지 설치 완료
echo.

:: .env 파일 생성
if not exist .env (
    if exist .env.example (
        echo [추가] .env 파일 생성 중...
        copy .env.example .env
        echo ✓ .env 파일이 생성되었습니다.
        echo ! .env 파일을 열어 필요한 설정을 입력하세요.
    )
)

echo.
echo ====================================
echo   환경 설정 완료!
echo ====================================
echo.
echo 다음 단계:
echo 1. .env 파일을 열어 설정을 확인하세요
echo 2. start_server.bat를 실행하여 서버를 시작하세요
echo.

pause
