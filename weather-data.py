import openaq
import sys
import requests

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

lat_long = query_lat_long(input)
print(lat_long)

#api = openaq.OpenAQ()
#status, resp = api.sources()
#res = resp['results']
#print(res)