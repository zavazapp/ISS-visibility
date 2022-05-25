import requests
import datetime as dt
import time
import math
import smtplib

MIN_DISTANCE = 10

MY_LAT = 43.3209
MY_LONG = 21.8954

MY_POS = MY_LAT, MY_LONG
PARAMS = {
    "lat": MY_LAT,
    "lon": MY_LONG,
    "formatted": 0
}
not_sent = True


def get_my_hour():
    return dt.datetime.now().hour


def get_sunset_hour():
    result = requests.get("https://api.sunrise-sunset.org/json", params=PARAMS).json()
    return int(dt.datetime.fromisoformat(result["results"]["sunset"]).hour)


def get_sunrise_hour():
    result = requests.get("https://api.sunrise-sunset.org/json", params=PARAMS).json()
    return int(dt.datetime.fromisoformat(result["results"]["sunrise"]).hour)


def is_dark():
    return not (get_sunset_hour() < get_my_hour() < get_sunrise_hour())


def print_console():
    print(f"My time: {get_my_hour()}")
    print(f"Sunset time: {get_sunset_hour()}")
    print(f"Sunrise time: {get_sunrise_hour()}")
    print(f"Dark = {is_dark()}")
    print(f"ISS position: {get_iss_position()}")
    print(f"My position: {MY_POS}")
    print(f"Distance = {get_distance()}")
    print(f"Is ISS visible: {is_iss_visible()}")


def is_iss_visible():
    return get_distance() < MIN_DISTANCE


def get_distance():
    return math.dist(MY_POS, get_iss_position())


def get_iss_position():
    result = requests.get("http://api.open-notify.org/iss-now.json").json()
    return float(result["iss_position"]["latitude"]), float(result["iss_position"]["longitude"])


while not_sent:
    time.sleep(5)
    print_console()
