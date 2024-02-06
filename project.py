"""
Aresh Tajvar, 2024
CS50 Python Final Project
Fed Weather

This program accesses the NOAA free and public-access API at https://api.weather.gov.

Prompts user for weather station per NOAA convention (ex: KSEA for Seattle, WA)
Return station name (ex: Seattle, Seattle-Tacoma International Airport)
Prompt user for desired weather detail (ex: temperature, barometricPressure)
Return selected weather detail (ex: Temperature: 13.7 degC)

Github repository:
https://github.com/AreTaj/fed-weather

Harvard CS50 Python Final Project:
https://cs50.harvard.edu/python/2022/project/

NOAA API Documentation:
https://www.weather.gov/documentation/services-web-api#/

NOAA Station Observations API:
https://api.weather.gov/stations/{station}/observations 

"""

import re
import sys
import requests


def main():
    station_input = input("Input a weather station: ")
    station_code = validate_station(station_input)          # If validated, station_input becomes station_code and is passed to station()
    station(station_code)

    properties_dict = api_and_parse(station_code)           # station_code is passed to api_and_parse(), which results properties_dict
    result, selection_data = get_weather(properties_dict)   # properties_dict is passed to get_weather(), which results result and selection_data
    format_and_print(result, selection_data)                # result and selection_data are passed to format_and_print()


def validate_station(station_input):
    example_stations = ["KBOS", "KNYC", "KOPF", "KHOU", "KABQ", "KSAN", "KLAX", "KSFO", "KPDX", "KSEA"]
    while True:
        if re.match("^[A-Z]{4}$", station_input):                                           # Standard is four capital letters
            station_check = requests.get(f"https://api.weather.gov/stations/{station_input}")
            if station_check.status_code != 200 and station_check.status_code != 404:       # Checks for API status; if not status_code = 200 (running), then kill
                sys.exit(f"Error: received status code {station_check.status_code}")
            elif station_check.status_code == 404:                                          # 404 indicates station does not exist in NOAA database, reprompt
                print(f"Incorrect station code. Try one of these: {example_stations}")
                station_input = input("Input a weather station: ")
                continue
            break
        else:                                                                               # If failed regex, reprompt
            print(f"Invalid station code. Try one of these: {example_stations}")
            station_input = input("Input a weather station: ")
            continue
    station_code = station_input                                                            # If and only if validation passed, station_input becomes station_code and is returned
    return station_code


def station(station_code):                                                                  # Gets station name from API, prints, returns station_name to facilitate testing
    station_response = requests.get(f"https://api.weather.gov/stations/{station_code}")
    station_data = station_response.json()
    station_properties = station_data["properties"]
    station_name = station_properties["name"]
    print(station_name)
    return station_name


def api_and_parse(station_code):
    response = requests.get(f"https://api.weather.gov/stations/{station_code}/observations")
    if response.status_code !=200:                              # Checks for API status; if not status_code = 200 (running), then kill
        sys.exit(f"Error: received status code {response.status_code}")
    else:
        data = response.json()                                  # dict
        features_list = data["features"]                        # list
        element_dict = features_list[0]                         # dict; always takes the first element because NWS has standardized format
        properties_dict = element_dict.get("properties")        # dict
        return properties_dict                                  # dict of all possible weather properties, passes to get_weather()


def get_weather(properties_dict):
    valid_properties_list = ["elevation", "temperature", "dewpoint", "windDirection", "windSpeed", "barometricPressure", "seaLevelPressure", "visibility", "relativeHumidity", "windChill"]
    selection = input(f"Valid options: {valid_properties_list}.\nInput weather property: ")
    while True:
        if selection in valid_properties_list:
            selection_data = properties_dict.get(selection)     # dict
            result = "".join(' ' + i if i.isupper() else i for i in selection).capitalize() # Ex: barometricPressure --> Barometric pressure, temperature --> Temperature
            break
        else:
            print("\nInvalid weather property")
            selection = input(f"Valid options: {valid_properties_list}.\nInput weather property: ")
            continue
    return result, selection_data


def format_and_print(result, selection_data):
    unit_code = str(selection_data.get("unitCode"))             # Take unitCode and convert to str
    units = unit_code.split(":")[1]                             # Split unit_code at ":", and only take whatever is to the right into units
    value = str(selection_data.get("value"))                    # Take value and convert to str
    print(result +": "+ value + " " + units)


if __name__ == "__main__":
    main()