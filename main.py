# coding=utf-8
import json
# sudo pip install request
import requests
import random
import time
import pprint
import sys
from argparse import ArgumentParser
from xml.dom import minidom

try:
    from urllib.request import urlopen
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlopen, urlencode

backendUrl = 'http://localhost:27301'
headers = {"Content-type": "application/json"}
r = lambda: random.randint(0, 255)

API_KEY = "" # Enter OpenWeather API key here
pp = pprint.PrettyPrinter(indent=4)


def set_color(x, y, color):
    signal = {
        'zoneId': str(x) + ',' + str(y),
        'color': color,
        'effect': 'SET_COLOR',
        'pid': 'DK4QPID',
        'clientName': 'philiip11'
    }
    signal_json = json.dumps(signal)
    res_signal = requests.post(backendUrl + '/api/1.0/signals', data=signal_json, headers=headers)
    # checking the response
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
                print "Error: " + res_signal.text
            time.sleep(0.01)


def random_colors():
    for y in range(0, 6):
        for x in range(0, 22):
            set_color(x, y, '#%02X%02X%02X' % (r(), r(), r()))


def get_current_weather(location):
    url = "https://api.openweathermap.org/data/2.5/weather?units=metric&APPID=" + API_KEY + '&' + urlencode(
        {"q": location})
    request = requests.get(url)
    if request.ok:
        weather_object = json.loads(request.text)
        # pp.pprint(weather_object)
        return weather_object["weather"][0]["icon"]


def get_color_from_weather(weather):
    return {
        "01d": "#ffff00",
        "02d": "#99ff33",
        "03d": "#666699",
        "04d": "#99ff33",
        "09d": "#00ffff",
        "10d": "#0066ff",
        "11d": "#ff0066",
        "13d": "#ffffff",
        "50d": "#cc33ff"
    }.get(weather, "#ff0000")


# random_colors()
# delete_all()
set_color(0, 0, get_color_from_weather(get_current_weather("Gaimersheim, DE")))
# get_weather("Gaimersheim, DE")
# get_weather("Sydney, AU")
