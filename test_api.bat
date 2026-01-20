@echo off
chcp 65001 >nul
echo.
echo [AdGen AI - API Test]
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

echo 서버가 실행 중인지 확인하세요 (http://127.0.0.1:8000)
echo.

:: 테스트 이미지 확인
if not exist test_images\sample.jpg (
    echo ✗ 테스트 이미지가 없습니다: test_images\sample.jpg
    echo test_images 폴더에 sample.jpg 파일을 준비하세요.
    pause
    exit /b 1
)

echo [1/3] Health Check...
curl -X GET http://127.0.0.1:8000/api/v1/health
echo.
echo.

echo [2/3] 이미지 정보 조회...
curl -X POST http://127.0.0.1:8000/api/v1/image-info ^
  -F "file=@test_images/sample.jpg"
echo.
echo.

echo [3/3] 배경 제거 테스트...
echo 결과는 test_output.png로 저장됩니다...
curl -X POST http://127.0.0.1:8000/api/v1/remove-background ^
  -F "file=@test_images/sample.jpg" ^
  -F "ratio=4:5" ^
  -F "style=minimal" ^
  --output test_output.png
echo.

if exist test_output.png (
    echo ✓ 배경 제거 성공! test_output.png 파일을 확인하세요.
    start test_output.png
) else (
    echo ✗ 배경 제거 실패
)

echo.
pause
