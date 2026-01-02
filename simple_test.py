import requests

url = "http://127.0.0.1:8000/api/v1/remove-background"
image_path = r"C:\Users\brook\.gemini\antigravity\brain\0bf53c44-76d6-485d-a482-b08aa93566f8\uploaded_image_1767315578522.png"

with open(image_path, 'rb') as f:
    files = {'file': f}
    data = {'ratio': '4:5'}
    
    response = requests.post(url, files=files, data=data, timeout=120)
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        with open('api_result.png', 'wb') as out:
            out.write(response.content)
        print("Success! Saved to api_result.png")
        print(f"Size: {len(response.content)} bytes")
    else:
        print(f"Error: {response.text}")
