import requests
import datetime
import urllib.parse
import os

GOOGLE_API_KEY = os.environ["GOOGLE_API_KEY"]
ZALO_ACCESS_TOKEN = os.environ["ZALO_TOKEN"]
ZALO_USER_ID = os.environ["ZALO_USER_ID"]

ORIGIN = "Trường Tiểu học Võ Thị Sáu Quận 7 TP HCM"
DESTINATION = "285 Cách Mạng Tháng 8 Quận 10 TP HCM"

def get_route():

    url = "https://maps.googleapis.com/maps/api/directions/json"

    params = {
        "origin": ORIGIN,
        "destination": DESTINATION,
        "departure_time": "now",
        "traffic_model": "best_guess",
        "mode": "driving",
        "key": GOOGLE_API_KEY
    }

    res = requests.get(url, params=params).json()

    leg = res["routes"][0]["legs"][0]

    duration = leg["duration_in_traffic"]["text"]

    link = "https://www.google.com/maps/dir/?api=1&origin=" + urllib.parse.quote(ORIGIN) + "&destination=" + urllib.parse.quote(DESTINATION)

    today = datetime.date.today().strftime("%d/%m/%Y")

    msg = f"""
🚦 LỘ TRÌNH ĐI LÀM {today}

Xuất phát
Trường Võ Thị Sáu Q7

Điểm đến
285 CMT8 Q10

Thời gian dự kiến
{duration}

Google Maps
{link}
"""

    return msg

def send_zalo(msg):

    url = "https://openapi.zalo.me/v2.0/oa/message"

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

    requests.post(url, headers=headers, json=data)

msg = get_route()
send_zalo(msg)
