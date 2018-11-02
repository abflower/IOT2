import datetime
import feedparser
from datetime import datetime
from flask import Flask
from flask import make_response
from flask import Markup
from flask import render_template
import json
import requests
#import urllib.request, urllib.error

import os
print (os.getcwd())

app = Flask(__name__)


# SOME VARIABLES USED IN THE CODE

# NEWS AND METEO PORTAL


CITIES = ['Bristol,UK', 'Palermo,IT']

#PUBLISHERS = ['Italy', 'United Kingdom']

RSS_FEEDS = {'Italy': 'http://www.televideo.rai.it/televideo/pub/rss120.xml',
             'UK': 'http://feeds.bbci.co.uk/news/rss.xml'}


# VARIABLES FOR IOT





# FUNCTIONS FOR PORTAL

def update_time():
    now = datetime.now()
    now = now.strftime("%Y-%m-%d %H:%M:%S")
    return now


def get_news(publisher):
    feed = feedparser.parse(RSS_FEEDS[publisher])
    return feed['entries']

def get_weather(query):
    api_key = 'ec4d49005a9bc48be23f2ce0d2503228'
    api_url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=' + api_key
    query_url = api_url.format(query)
    try:
        uh = requests.get(query_url)
        data = uh.content
    #uh = urllib.request.urlopen(query_url)
    #data = uh.read().decode()
    # print(data)
        parsed = json.loads(data)
        weather = None
        if parsed.get("weather"):
            url = '<img src="http://openweathermap.org/img/w/'
            icon_url = url + parsed["weather"][0]["icon"] + '.png">'
            icon_url = Markup(icon_url)
            min = str(parsed["main"]["temp_min"])
            if len(min) == 1:
                min = '0'+min
            else:
                pass
            max = str(parsed["main"]["temp_max"])
            if len(max) == 1:
                max = '0' + max
            else:
                pass

            weather = {
                "name": parsed["name"],
                "temperature": parsed["main"]["temp"],
                "symbol": icon_url,
                "description": parsed["weather"][0]["description"],
                "min": min,
                "max": max,
                "hum": parsed["main"]["humidity"],
                "pressure": parsed["main"]["pressure"]}
        return weather
    except:
        weather = {
            "name": "Error",
            "temperature": "0",
            "symbol": '<img src="https://openweathermap.org/img/w/10d.png">',
            "description": "Error",
            "min": "0",
            "max": "0",
            "pressure": "0"}
        return weather




def get_meteo():
    meteo = []
    for city in CITIES:
       meteo.append(get_weather(city))
    return meteo


# FUNCTIONS RELATIVE TO IOT

def read_json():
    try:
        with open('/var/www/myapp/IOT2/files/datatrasf.json', 'r') as f:
            data = json.load(f)
            return data
    except:
        data = {"sensor":{"temp":0.0, "hum":0}, "automations":[], "check":"Error in retrieving data"}
        return data



# ------------------ THE FLASK APP -----------------

@app.route("/")
def home():

    time = update_time()
    meteo = get_meteo()
    news_ITA = get_news('Italy')
    news_UK = get_news('UK')
    data = read_json()
    t_and_u = data['sensor']
    automations = data['automations']
    check = data['check']
    response = make_response(render_template("index.html", time=time, news_ITA=news_ITA, news_UK=news_UK,
                                             meteo=meteo, t_and_u=t_and_u, automations=automations, check=check))
    return response

if __name__ == "__main__":
    app.run(port=5000, debug=True)
