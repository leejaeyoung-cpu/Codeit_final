"""
API 엔드포인트 테스트 스크립트
"""
import requests
import time

print("="*60)
print("API 엔드포인트 검증 테스트")
print("="*60)

# 1. 헬스체크
print("\n1. Health Check 테스트...")
try:
    response = requests.get("http://127.0.0.1:8000/health")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# 2. Root 엔드포인트
print("\n2. Root 엔드포인트 테스트...")
try:
    response = requests.get("http://127.0.0.1:8000/")
    print(f"   Status: {response.status_code}")
    data = response.json()
    print(f"   Message: {data.get('message')}")
    print(f"   Version: {data.get('version')}")
    print(f"   Endpoints:")
    for key, value in data.get('endpoints', {}).items():
        print(f"      - {key}: {value}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# 3. API Health 엔드포인트
print("\n3. API Health 엔드포인트 테스트...")
try:
    response = requests.get("http://127.0.0.1:8000/api/v1/health")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# 4. 배경 제거 API 테스트
print("\n4. 배경 제거 API 테스트...")
test_image_path = "C:/Users/brook/.gemini/antigravity/brain/0bf53c44-76d6-485d-a482-b08aa93566f8/uploaded_image_1767315578522.png"

try:
    print(f"   이미지: {test_image_path}")
    
    files = {'file': open(test_image_path, 'rb')}
    data = {'ratio': '4:5'}
    
    print("   요청 전송 중...")
    start_time = time.time()
    response = requests.post(
        "http://127.0.0.1:8000/api/v1/remove-background",
        files=files,
        data=data,
        timeout=60
    )
    elapsed = time.time() - start_time
    
    print(f"   Status: {response.status_code}")
    print(f"   처리 시간: {elapsed:.2f}s")
    print(f"   Content-Type: {response.headers.get('Content-Type')}")
    print(f"   X-Processing-Time: {response.headers.get('X-Processing-Time')}s")
    
    if response.status_code == 200:
        # 결과 저장
        output_path = "api_test_result.png"
        with open(output_path, 'wb') as f:
            f.write(response.content)
        print(f"   ✅ 결과 저장: {output_path} ({len(response.content)} bytes)")
    else:
        print(f"   ❌ Error: {response.text}")
        
except Exception as e:
    print(f"   ❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*60)
print("테스트 완료")
print("="*60)
