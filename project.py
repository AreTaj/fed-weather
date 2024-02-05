"""
Aresh Tajvar, 2024
CS50 Python Final Project
Fed Weather

This program accesses the NOAA free and public-access API at https://api.weather.gov.

Prompts user for weather station per NOAA convention (ex: KSEA for Seattle, WA)
Return station name (ex: Seattle, Seattle-Tacoma International Airport)
Prompt user for desired weather detail (ex: temperature, barometricPressure)
Return selected weather detail (ex: Temperature: 13.7 degC)

Harvard CS50 Final Project:
https://cs50.harvard.edu/python/2022/project/

Github repository:
https://github.com/AreTaj/fed-weather

NOAA API Documentation:
https://www.weather.gov/documentation/services-web-api#/

NOAA Station Observations API:
https://api.weather.gov/stations/{station}/observations 

"""

import re
import sys
import requests


def main():
    #station()
    #api_and_parse()
    #user_input()
    format_and_print()


def station():
    example_stations = ["KBOS", "KNYC", "KRIC", "KOPF", "KHOU", "KABQ", "KSAN", "KLAX", "KSFO", "KPDX", "KSEA"]
    while True:
        station = input("Input a weather station: ")
        if re.match("^[A-Z]{4}$", station):
            station_response = requests.get(f"https://api.weather.gov/stations/{station}")
            if station_response.status_code != 200 and station_response.status_code != 404:     # Checks for API status; if not status_code = 200 (running), then kill
                sys.exit(f"Error: received status code {station_response.status_code}")
            elif station_response.status_code == 404:
                print(f"Incorrect station code. Try one of these: {example_stations}")
                continue
            break
        else:
            print(f"Invalid station code. Try one of these: {example_stations}")
            continue
    station_data = station_response.json()
    station_properties = station_data["properties"]
    station_name = station_properties["name"]
    print(station_name)
    return station


def api_and_parse():
    station_id = station()
    response = requests.get(f"https://api.weather.gov/stations/{station_id}/observations")
    if response.status_code !=200:      # Checks for API status; if not status_code = 200 (running), then kill
        sys.exit(f"Error: received status code {response.status_code}")
    else:
        data = response.json()                          # dict
        features_list = data["features"]                    # list
        element_dict = features_list[0]                         # dict; always takes the first element because NWS has standardized format
        properties_dict = element_dict.get("properties")    # dict
        #print(properties_dict.keys())
        return properties_dict


def user_input():
    properties = api_and_parse()
    while True:
        valid_properties_list = ["elevation", "temperature", "dewpoint", "windDirection", "windSpeed", "barometricPressure", "seaLevelPressure", "visibility", "relativeHumidity", "windChill"]
        selection = input("Valid property options: elevation, temperature, dewpoint, windDirection, windSpeed, barometricPressure, seaLevelPressure, visibility, relativeHumidity, windChill.\nInput weather property: ")
        if selection in valid_properties_list:
            selection_data = properties.get(selection)     # dict
            # Below two lines are to format selection for readability. Ex: barometricPressure --> Barometric pressure, temperature --> Temperature
            result = "".join(' ' + i if i.isupper() else i for i in selection).capitalize()
            break
        else:
            print("\nInvalid weather property")
            continue
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