import requests
result = requests.get("http://127.0.0.1:8001/parking_spots")
print(result.json()[0])