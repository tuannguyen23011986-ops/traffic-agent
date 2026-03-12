import requests
import os
import datetime

API_KEY = os.getenv("GOOGLE_API_KEY")
ZALO_ACCESS_TOKEN = os.getenv("ZALO_TOKEN")
ZALO_USER_ID = os.getenv("ZALO_USER_ID")

origin = "Trường Tiểu học Võ Thị Sáu Quận 7 TP HCM"
destination = "285 Cách Mạng Tháng 8 Quận 10 TP HCM"

url = "https://routes.googleapis.com/directions/v2:computeRoutes"

headers = {
    "Content-Type": "application/json",
    "X-Goog-Api-Key": API_KEY,
    "X-Goog-FieldMask": "routes.duration,routes.distanceMeters"
}

data = {
  "origin": {"address": origin},
  "destination": {"address": destination},
  "travelMode": "DRIVE",
  "routingPreference": "TRAFFIC_AWARE"
}

res = requests.post(url, headers=headers, json=data).json()

if "routes" not in res:
    print("Google API không trả dữ liệu:", res)
    exit(1)

duration = res["routes"][0]["duration"]
seconds = int(duration.replace("s",""))
minutes = int(seconds/60)

today = datetime.date.today()

msg = f"""
🚦 Lộ trình đi làm {today}

Xuất phát:
Trường Võ Thị Sáu Q7

Điểm đến:
285 CMT8 Q10

Thời gian dự kiến:
{minutes} phút
"""

zalo_url = "https://openapi.zalo.me/v2.0/oa/message"

headers = {"access_token": ZALO_ACCESS_TOKEN}

data = {
  "recipient":{"user_id":ZALO_USER_ID},
  "message":{"text":msg}
}

requests.post(zalo_url,headers=headers,json=data)
