from pandas.core.frame import DataFrame
import pandas as pd
import openaq
import requests
from datetime import datetime as dt
from datetime import date
from datetime import timedelta
from meteostat import Point
from meteostat import Daily 

cities_of_interest = {"Akureyri": "IS", "London": "GB", 
    "Mexico City": "MX", "Newcastle": "GB", "Reykjavík":"IS"}
data_dirs = {"weather": "data/weather", "pollution": "data/pollution"}

def fetch_weather_data(city_name, date_from=date.today() - timedelta(30), date_to=date.today()):
    ''' Fetch weather measurements for a particular city during a particular time.

    '''
    #We limit to the 5 cities above
    city_and_country = sanitize_city(city_name)

    #Since both the weather api and pandas dataframe operate on the datetime level
    #cast date to datetime early 
    midnight_time = dt.min.time()
    dt_from = dt.combine(date_from, midnight_time)
    dt_to = dt.combine(date_to, midnight_time)

    weather = fetch_weather_from_csv(city_and_country[0], dt_from= dt_from, dt_to=dt_to)

    if(weather.empty):
        weather = fetch_weather_from_api(city_and_country, dt_from, dt_to)
    #The complicated case is: a file exists but not all the data is there
    elif(needs_more_data(weather, dt_from, dt_to)):
        weather = partial_csv_update(city_and_country, dt_from, dt_to)
    return weather

def fetch_pollution_data(city_name, date_fromd=date.today() - timedelta(days=30), date_to=date.today()):
    return "some pollution"

def needs_more_data(data, dt_from, dt_to):
    delta_days = (dt_to - dt_from).days + 1
    data_subset = data[(dt_from <= data.index) & (data.index <= dt_to)]
    return len(data_subset) < delta_days

def sanitize_city(city_name):
    if city_name not in cities_of_interest.keys():
        raise Exception(f"Please enter one of {cities_of_interest}.")
    return (city_name, cities_of_interest[city_name])

def fetch_weather_from_csv(city_name, **kwargs):
    file_dir = data_dirs["weather"]
    
    #Empty dataframe for when there is no csv file
    weather_data = pd.DataFrame({'' : []})

    try:
        weather_data = pd.read_csv(f'{file_dir}/{city_name}.csv', index_col='date', parse_dates=['date'])
        if (kwargs):
            return weather_data[(kwargs['dt_from'] <= weather_data.index) & (weather_data.index <= kwargs['dt_to'])]
    except FileNotFoundError:
        print("No historical weather data found locally. Using API to get fresh data.")
    return weather_data

def fetch_weather_from_api(city_and_country, date_from, date_to):
    # The first part of the tuple is the city and our csv data is organized by city name.
    city_coords = query_lat_long(city_and_country)
    data = query_historical_weather(city_coords, date_from, date_to)

    #Write new csv file
    dir_name = data_dirs['weather']
    data.to_csv(f'{dir_name}/{city_and_country[0]}.csv')
    return data

def partial_csv_update(city_and_country, dt_from, dt_to):
    #Note that this is all of our CSV data for the city. no time filter
    from_file = fetch_weather_from_csv(city_and_country[0])

    #We time filter here because we know the missing data is in the range [dt_from, dt_to]
    from_api = fetch_weather_from_api(city_and_country, dt_from, dt_to)
    total_data = pd.concat([from_file, from_api])
    unique_days = total_data.drop_duplicates()
    unique_days = unique_days.sort_values('date')

    dir_name = data_dirs['weather']
    unique_days.to_csv(f'{dir_name}/{city_and_country[0]}.csv')
    return unique_days

def filter_results_to_country(geoapi_response_data, country):
    #If there are multiple cities with the same name, we choose the most populated
    filter_by_country = [resp for resp in geoapi_response_data if resp['country_code'] == country]
    # 
    sorted_by_pop = sorted(filter_by_country, key = lambda resp: resp['population'] if 'population' in resp else 0, reverse=True)
    result = sorted_by_pop[0]

    # Relevant subset of the result dict
    return {key: result[key] for key in ('latitude', 'longitude', 'elevation', 'population')}

def query_lat_long(city_country):
    params_dict = {
        'name': city_country[0],
        #Default is 10 but since newcastle gives 9, we might hit the limit
        'count': 100
    }

    # Since the user gives us more than 3 chars, the api performs fuzzy matching. So we do not
    # need to worry abt spelling
    resp = requests.get('https://geocoding-api.open-meteo.com/v1/search', params_dict)
    data = resp.json()
    
    return filter_results_to_country(data['results'], city_country[1])

def query_historical_weather(lat_long_elevation, date_from, date_to):
    # Since we have dates and the api uses time, we need to convert from date to datetime
    midnight_time = dt.min.time()
    dt_from = dt.combine(date_from, midnight_time)
    dt_to = dt.combine(date_to, midnight_time)
    
    location = Point(
        lat_long_elevation['latitude'], 
        lat_long_elevation['longitude'], 
        lat_long_elevation['elevation'])

    daily = Daily(location, start=dt_from, end=dt_to)
    
    # Ask meteostat to fill in any gaps in the data
    daily.normalize()
    data = daily.fetch()
    
    #tavg=Temp average (C).prcp=Total precipitation(mm). wdir=Wind direction(degrees)
    #wspd=Average wind speed(km/h).wpgt=Wind peak gust(km/hr). pres=Sea-level air pressure(hpa)
    #rhum=Relative humidity(does not work)
    response = data[['tavg', 'prcp', 'wdir', 'wspd', 'wpgt', 'pres']]

    #Since time is an index, simply calling rename does not work
    tidy = response.rename_axis(index={"time": "date"})

    return tidy

def get_weather(city_country):
    coords = query_lat_long(city_country)
    return query_historical_weather(coords)


#From fetching measurements data notebook

# TODO
# 1. Drop the ID column, don't need to write that into the file
# 2. The dates are not the same for all cities.. Look into that
# 3. Maybe count locations and provide that into the dataframe as well. 
#    It's relevent to know how many measures are in the city.
# 4. Can we choose certain type of measures

# Filter what city we want to get
def filter_results_to_country(geoapi_response_data, country):
    #If there are multiple cities with the same name, we choose the most populated
    filter_by_country = [resp for resp in geoapi_response_data if resp['country_code'] == country]
    # 
    sorted_by_pop = sorted(filter_by_country, key = lambda resp: resp['population'] if 'population' in resp else 0, reverse=True)
    result = sorted_by_pop[0]

    # Relevant subset of the result dict
    return {key: result[key] for key in ('latitude', 'longitude', 'elevation', 'population')}

def measurement_to_csv(city_country, date_from, date_to):
    '''
    This function takes in a city, parameter and date and writes data into a csv.file
    Input:
        city: name of a city (string)
        ???parameter: List of strings that represent the parameters wanted to calculate
        date_from: measurments after this date will be calculated
        date_to: Measures until this date will be calculated
    '''
    
    # Fetch the api
    # http://dhhagan.github.io/py-openaq/api.html
    api = openaq.OpenAQ(version ='v2')
    # Get the longitude and latitude for the city
    location = query_lat_long(city_country)
    coords = f'{location["latitude"]},{location["longitude"]}'
    
    # Call the location api to check for the first date updated
    locations = api.locations(coordinates = coords,radius = 10000,df = True)

    min_date = locations["firstUpdated"].min()
    
    min_date = min_date.tz_convert(None)
    
    min_date = pd.to_datetime(min_date) 
    
    if min_date > date_from:
        date_from = min_date
    
    
    # Number of days we want measurements for
    day_diff = (date_to - date_from).days
    
    # How we split the call between days to the API
    split_days = 30

    # Number of 30 day blocks in our range
    number_months = day_diff // split_days

    # Initialize the start date
    start = date_from

    # Add measurements to csv file 30 days at a time
    # An extra iteration for the remaining <30 days
    for n in range(number_months + 1):
        
        # Find the end date
        end = start + dt.timedelta(days = split_days)
        
        # Fetch the data from the measurment api
        df_api = api.measurements(coordinates = coords, radius = 5000, df = True, 
                                  limit = 30000, parameter = ["pm25", "pm10"], value_from = 0,
                              date_from = start, date_to = end)
        
        # Start as the last end date
        start = end

        # For the first iteration create df
        if n == 0: 
            df = df_api.copy()
        # After the first iteration append the data
        else:
            df = df.append(df_api)
    
    ## Data prepping 

    # Change the index
    df.index.name = 'Date.local'
    df.reset_index(inplace=True)
    df['Date'] = df['Date.local'].dt.strftime('%Y-%m-%d')
    df['value'] = df['value'].astype(float, errors = 'raise')

    # Calculate mean, max and min value for each date
    Result_mean = df.groupby(['Date', 'parameter'],as_index=False)['value'].mean()
    Result_max = df.groupby(['Date', 'parameter'],as_index=False)['value'].max()
    Result_min = df.groupby(['Date', 'parameter'],as_index=False)['value'].min()

    # Pivot the tables to wide format
    ResultWide_mean = Result_mean.pivot_table(index='Date',columns='parameter', values='value')
    ResultWide_max = Result_max.pivot_table(index='Date',columns='parameter', values='value')
    ResultWide_min = Result_min.pivot_table(index='Date',columns='parameter', values='value')

    # Rename the columns to distinguish
    ResultWide_mean.rename(columns={"pm10": 'pm10_mean', 'pm25': 'pm25_mean'}, inplace=True)
    ResultWide_max.rename(columns={"pm10": 'pm10_max', 'pm25': 'pm25_max'}, inplace=True)
    ResultWide_min.rename(columns={"pm10": 'pm10_min', 'pm25': 'pm25_min'}, inplace=True)

    # Join mean and max first
    df_first_join = pd.merge(ResultWide_mean, ResultWide_max, left_index=True, right_index=True)

    # Join now to min
    ResultWide = pd.merge(df_first_join, ResultWide_min, left_index=True, right_index=True)

    # Change the index (Can we drop the ID column?)
    ResultWide.index.name = 'Date'
    ResultWide.reset_index(inplace=True)
    ResultWide.index.name = 'ID'

    # Write to a file  
    Path = f'Data_measurements/{city_country}.csv'
    ResultWide.to_csv(Path)
    
    
# Call the function
city = 'London'
date_from = pd.to_datetime('2020-01-01') 
date_to = pd.to_datetime('2021-05-01')

#measurement_to_csv(city,date_from,date_to)
data = fetch_weather_data(city, date_from=date.today() - timedelta(days=365))