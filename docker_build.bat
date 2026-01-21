@echo off
chcp 65001 >nul
echo.
echo [AdGen AI - Docker Build and Run]
echo.
echo.

:: Docker 실행 여부 확인
echo [1/4] Docker 확인 중...
docker --version >nul 2>&1
if errorlevel 1 (
    echo ✗ Docker가 설치되어 있지 않거나 실행 중이 아닙니다.
    echo Docker Desktop을 설치하고 실행하세요.
    pause
    exit /b 1
)
echo ✓ Docker 확인 완료
echo.

:: 기존 컨테이너 중지 및 제거
echo [2/4] 기존 컨테이너 정리 중...
docker-compose down
echo ✓ 정리 완료
echo.

:: Docker 이미지 빌드
echo [3/4] Docker 이미지 빌드 중...
echo 이 작업은 몇 분 정도 걸릴 수 있습니다...
docker-compose build
if errorlevel 1 (
    echo ✗ 빌드 실패
    pause
    exit /b 1
)
echo ✓ 빌드 완료
echo.

:: 컨테이너 실행
echo [4/4] 컨테이너 실행 중...
docker-compose up -d
if errorlevel 1 (
    echo ✗ 실행 실패
    pause
    exit /b 1
)

echo.
echo ====================================
echo   Docker 컨테이너 실행 완료!
echo ====================================
echo.
echo 서버 주소: http://localhost:8000
echo Swagger UI: http://localhost:8000/docs
echo.
echo 컨테이너 로그 확인: docker-compose logs -f
echo 컨테이너 중지: docker-compose down
echo.

pause
