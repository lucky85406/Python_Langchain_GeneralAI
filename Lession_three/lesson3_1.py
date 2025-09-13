import requests
response = requests.get("https://www.yahoo.com")
print(f"回應狀態碼：{response.status_code}")
print(f"回應的前100字元：{response.text[:100]}")