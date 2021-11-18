import openaq
import sys
import requests
import datetime as dt

openweathermap_api_key = '8894806b2a698231a8197f03b65d4762'
cities_of_interest = {"Akureyri": "IS", "London": "GB", 
    "Mexico City": "MX", "Newcastle": "GB", "Reykjavík":"IS"}

input = "Mexico City" #input(f"Please enter one of {cities_of_interest} \n")

if input not in cities_of_interest.keys():
    raise Exception("Bad user, give me the city")

def filter_results_to_country(geoapi_response_data):
    print("fubbus")
    #1 fish out the coords and population
    #2 order by pop and return first item.

def query_lat_long(name):
    #TODO: CACHE?
    params_dict = {
        'name': name,
        #Default is 10 but since newcastle gives 9, we might hit the limit
        'count': 100
    }

    # Since the user gives us more than 3 chars, the api performs fuzzy matching. So we do not
    # need to worry abt spelling
    resp = requests.get('https://geocoding-api.open-meteo.com/v1/search', params_dict)
    data = resp.json()
    
    return filter_results_to_country(data['results'])

def query_historical_weather(city_and_country):
    now = dt.datetime.now()
    five_day_delta = dt.timedelta(days=4)
    five_days_ago = now - five_day_delta
    five_days_ago_unix = int(five_days_ago.timestamp())

    city_country = "London,UK"
    params_dict = {
        'lat': '51.509865',
        'lon': '-0.136439',
        'units': 'metric',
        'dt': five_days_ago_unix,
        'appid': openweathermap_api_key
    }
        #lat={lat}&lon={lon}&dt={time}&appid={API key}

    resp = requests.get('https://api.openweathermap.org/data/2.5/onecall/timemachine', params_dict)

    print("fubbus")


lat_long = query_historical_weather(input)
print(lat_long)

#api = openaq.OpenAQ()
#status, resp = api.sources()
#res = resp['results']
#print(res)