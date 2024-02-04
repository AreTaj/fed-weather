"""
https://cs50.harvard.edu/python/2022/project/

"""

import requests
import csv
# Maybe import BeautifulSoup

"""
Prompt user for weather station per NOAA convention (ex: KCRQ)
Return station name (ex: McClellan-Palomar Airport), then:
Prompt user for desired weather detail(s)

"""

# https://www.weather.gov/documentation/services-web-api#/
# https://api.weather.gov/stations/KCRQ/observations 

def main():
    #station()
    #api_and_parse()
    #user_input()
    format_and_print()

def station():      # Need to include station input validation
    station = input("Input a weather station: ")
    return station

def api_and_parse():
    station_id = station()
    response = requests.get(f"https://api.weather.gov/stations/{station_id}/observations")
    data = response.json()                          # dict
    features_list = data["features"]                    # list
    element_dict = features_list[0]                         # dict; takes the first element as NWS has standardized format
    #print(features_list)
    properties_dict = element_dict.get("properties")    # dict
    return properties_dict

def user_input():
    # ("Enter a weather property from this list: temperature, barometricPressure, dewpoint /n Weather Property: ")
    properties = api_and_parse()
    selection = input("Weather property: ")
    selection_data = properties.get(selection)     # dict
    # Below two lines are to format selection for readability. Ex: barometricPressure --> Barometric pressure, temperature --> Temperature
    s = selection
    result = "".join(' ' + i if i.isupper() else i for i in s).capitalize()
    return result, selection_data

def format_and_print():
    pass_through = user_input()
    result = pass_through[0]
    selection_data = pass_through[1]
    unit_code = str(selection_data.get("unitCode"))     # Take unitCode and convert to str
    units = unit_code.split(":")[1]                     # Split unit_code at ":", and only take whatever is to the right into units
    value = str(selection_data.get("value"))            # Take value and convert to str
    #quality_control = selection_data.get("qualityControl")

    print(result +": "+ value + " " + units)



if __name__ == "__main__":
    main()



"""
# Old code for cannibalizing

def weather():
    station_id = station()
    response = requests.get(f"https://api.weather.gov/stations/{station_id}/observations")
    data = response.json()
    return data

def select_weather():
    weather_data = weather()
    selection = input("Input a selection: ")
    select_weather = weather_data["barometricPressure"]
    return select_weather

with open('file.csv', 'w') as file:
    csv.writer(file)
    writerow()
"""