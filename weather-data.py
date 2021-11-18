import sys
from pandas.core.frame import DataFrame
import requests
import datetime as dt
from meteostat import Point
from meteostat import Daily 
import matplotlib.pyplot as plt

cities_of_interest = {"Akureyri": "IS", "London": "GB", 
    "Mexico City": "MX", "Newcastle": "GB", "Reykjavík":"IS"}

input = input(f"Please enter one of {cities_of_interest} \n")

if input not in cities_of_interest.keys():
    raise Exception("Bad user, give me the city")

def filter_results_to_country(geoapi_response_data, city):
    #If there are multiple cities with the same name, we choose the most populated
    filter_by_country = [resp for resp in geoapi_response_data if resp['country_code'] == cities_of_interest[city]]
    # 
    sorted_by_pop = sorted(filter_by_country, key = lambda resp: resp['population'] if 'population' in resp else 0, reverse=True)
    result = sorted_by_pop[0]

    # Relevant subset of the result dict
    return {key: result[key] for key in ('latitude', 'longitude', 'elevation', 'population')}

def query_lat_long(city):
    params_dict = {
        'name': city,
        #Default is 10 but since newcastle gives 9, we might hit the limit
        'count': 100
    }

    # Since the user gives us more than 3 chars, the api performs fuzzy matching. So we do not
    # need to worry abt spelling
    resp = requests.get('https://geocoding-api.open-meteo.com/v1/search', params_dict)
    data = resp.json()
    
    return filter_results_to_country(data['results'], city)

def query_historical_weather(lat_long_elevation):
    now = dt.datetime.now()
    three_year_weeks = 52*3
    three_year_delta = dt.timedelta(weeks=three_year_weeks)
    five_days_ago = now - three_year_delta 
    location = Point(
        lat_long_elevation['latitude'], 
        lat_long_elevation['longitude'], 
        lat_long_elevation['elevation'])

    daily = Daily(location, start=five_days_ago, end=now)
    
    # Ask meteostat to fill in any gaps in the data
    daily.normalize()
    data = daily.fetch()
    
    #tavg=Temp average (C).prcp=Total precipitation(mm). wdir=Wind direction(degrees)
    #wspd=Average wind speed(km/h).wpgt=Wind peak gust(km/hr). pres=Sea-level air pressure(hpa)
    return data[['tavg', 'prcp', 'wdir', 'wspd', 'wpgt', 'pres']]

def get_weather(city_country):
    coords = query_lat_long(city_country)
    return query_historical_weather(coords)

data = get_weather(input)
print(data)