@echo off
chcp 65001 >nul
echo.
echo [AdGen AI - Run Tests]
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

echo [1/2] 단위 테스트 실행 중...
pytest tests/ -v --tb=short
if errorlevel 1 (
    echo.
    echo ✗ 테스트 실패
    pause
    exit /b 1
)

echo.
echo [2/2] 커버리지 테스트 실행 중...
pytest --cov=app tests/ --cov-report=html
echo ✓ 커버리지 리포트 생성: htmlcov/index.html

echo.
echo ====================================
echo   테스트 완료!
echo ====================================
echo.

pause
