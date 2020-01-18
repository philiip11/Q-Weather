# coding=utf-8
import json
# sudo pip install request
import requests
import random
import time
import pprint
from datetime import datetime

try:
    from urllib.request import urlopen
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlopen, urlencode

location = "Sydney, AU"
backendUrl = 'http://localhost:27301'
headers = {"Content-type": "application/json"}

API_KEY = open("api.key", 'r').read(1024)
pp = pprint.PrettyPrinter(indent=4)

RESET = '\033[0m'

q = 1  # change to 0 for das keyboard 4q


def r():
    return random.randint(0, 255)


def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[iterator:iterator + lv // 3], 16) for iterator in range(0, lv, lv // 3))


def get_color_escape(red, green, blue, background=False):
    return '\033[{};2;{};{};{}m'.format(48 if background else 38, red, green, blue)


def get_color_escape_hex(hex_color):
    colors = hex_to_rgb(hex_color)
    return get_color_escape(colors[0], colors[1], colors[2], )


def set_color(x, y, color, desc):
    signal = {
        'zoneId': str(x) + ',' + str(y),
        'color': color,
        'effect': 'SET_COLOR',
        'pid': 'DK4QPID',
        'name': desc,
        'clientName': 'philiip11'
    }
    signal_json = json.dumps(signal)
    res_signal = requests.post(backendUrl + '/api/1.0/signals', data=signal_json, headers=headers)
    print ("set color of " + str(x) + ',' + str(y) + " to "
           + get_color_escape_hex(color)
           + color + RESET + " (" + desc + ")")
    if not res_signal.ok:
        print "Error: " + res_signal.text
    time.sleep(0.01)


def delete_all():
    for y in range(0, 6):
        for x in range(0, 22):
            zone_id = str(x) + ',' + str(y)
            res_signal = requests.delete(backendUrl + '/api/1.0/signals' + '/pid/DK4QPID/zoneId/' + zone_id,
                                         headers=headers)
            if not res_signal.ok:
                print ("Error: " + res_signal.text)
            time.sleep(0.01)


def random_colors():
    for y in range(0, 6):
        for x in range(0, 22):
            set_color(x, y, '#%02X%02X%02X' % (r(), r(), r()), None)


def get_current_weather(c_location):
    url = "https://api.openweathermap.org/data/2.5/weather?units=metric&lang=de&APPID=" + API_KEY + '&' + urlencode(
        {"q": c_location})
    request = requests.get(url)
    if request.ok:
        weather_object = json.loads(request.text)
        # pp.pprint(weather_object)
        return weather_object


def get_forecast_weather(c_location):
    url = "https://api.openweathermap.org/data/2.5/forecast?units=metric&lang=de&APPID=" + API_KEY + '&' + urlencode(
        {"q": c_location})
    request = requests.get(url)
    if request.ok:
        weather_object = json.loads(request.text)
        # pp.pprint(weather_object)
        return weather_object


def get_color_from_weather(weather):
    result = {
        "01d": "#ffff00",
        "02d": "#99ff33",
        "03d": "#666699",
        "04d": "#99ff33",
        "09d": "#00ffff",
        "10d": "#0066ff",
        "11d": "#ff0066",
        "13d": "#ffffff",
        "50d": "#cc33ff",
        "01n": "#777700",
        "02n": "#4c7f19",
        "03n": "#33334c",
        "04n": "#4c7f19",
        "09n": "#007777",
        "10n": "#003377",
        "11n": "#770033",
        "13n": "#777777",
        "50n": "#661977"
    }.get(weather, "#ff0000")
    if result == "#ff0000":
        print ("Fehler: " + weather)
    return result


# random_colors()
# delete_all()

while True:
    current_weather = get_current_weather(location)
    current_weather_color = get_color_from_weather(current_weather["weather"][0]["icon"])
    current_weather_text = current_weather["weather"][0]["description"] + " (" + datetime.fromtimestamp(
        int(current_weather["dt"])).strftime("%H:%M:%S Uhr %d.%m.") + ")"
    set_color(q, 0, current_weather_color, current_weather_text)

    forecast = get_forecast_weather(location)
    for i in range(0, 15):
        i_weather = forecast["list"][i]["weather"][0]
        i_time = datetime.fromtimestamp(int(forecast["list"][i]["dt"])).strftime("%H Uhr %d.%m.")
        key = i + 2 + q
        if key > 5 + q:
            key = key + 1

        i_weather_color = get_color_from_weather(i_weather["icon"])
        i_weather_text = i_weather["description"] + " (" + i_time + ")"
        set_color(key, 0, i_weather_color, i_weather_text)
    time.sleep(600)  # Wait 10 minutes
