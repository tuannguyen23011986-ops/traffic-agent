import requests
import datetime
import urllib.parse
import os

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
ZALO_ACCESS_TOKEN = os.getenv("ZALO_TOKEN")
ZALO_USER_ID = os.getenv("ZALO_USER_ID")

origin = "Trường Tiểu học Võ Thị Sáu Quận 7 TP HCM"
destination = "285 Cách Mạng Tháng 8 Quận 10 TP HCM"

url = "https://maps.googleapis.com/maps/api/directions/json"

params = {
    "origin": origin,
    "destination": destination,
    "departure_time": "now",
    "key": GOOGLE_API_KEY
}

res = requests.get(url, params=params).json()

if "routes" not in res or len(res["routes"]) == 0:
    print("Google Maps API không trả dữ liệu")
    exit(1)

leg = res["routes"][0]["legs"][0]

duration = leg["duration"]["text"]

link = f"https://www.google.com/maps/dir/?api=1&origin={urllib.parse.quote(origin)}&destination={urllib.parse.quote(destination)}"

today = datetime.date.today()

msg = f"""
🚦 Lộ trình đi làm {today}

Xuất phát
Trường Võ Thị Sáu Q7

Điểm đến
285 CMT8 Q10

Thời gian dự kiến
{duration}

Google Maps
{link}
"""

zalo_url = "https://openapi.zalo.me/v2.0/oa/message"

headers = {
    "access_token": ZALO_ACCESS_TOKEN
}

data = {
    "recipient": {
        "user_id": ZALO_USER_ID
    },
    "message": {
        "text": msg
    }
}

requests.post(zalo_url, headers=headers, json=data)
