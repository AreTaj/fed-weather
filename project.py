"""
https://cs50.harvard.edu/python/2022/project/
https://github.com/AreTaj/fed-weather

"""
import re
import sys
import requests

"""
Prompt user for weather station per NOAA convention (ex: KSEA)
Return station name (ex: Seattle, Seattle-Tacoma International Airport), then:
Prompt user for desired weather detail(s)

"""

# https://www.weather.gov/documentation/services-web-api#/
# https://api.weather.gov/stations/KSEA/observations 

def main():
    #station()
    #api_and_parse()
    #user_input()
    format_and_print()


def station():      # Needs input validation 
    while True:
        station = input("Input a weather station: ")
        if re.match("^[A-Z]{4}$", station):
            break
        else:
            print("Invalid input, please try again.")
    return station


def api_and_parse():
    station_id = station()
    station_response = requests.get(f"https://api.weather.gov/stations/{station_id}")
    if station_response.status_code != 200:     # Checks for API status; if not status_code = 200 (running), then kill
        sys.exit(f"Error: received status code {station_response.status_code}")
    else:
        station_data = station_response.json()
        station_properties = station_data["properties"]
        station_name = station_properties["name"]
        print(station_name)

    response = requests.get(f"https://api.weather.gov/stations/{station_id}/observations")
    if response.status_code !=200:      # Checks for API status; if not status_code = 200 (running), then kill
        sys.exit(f"Error: received status code {response.status_code}")
    else:
        data = response.json()                          # dict
        features_list = data["features"]                    # list
        element_dict = features_list[0]                         # dict; takes the first element as NWS has standardized format
        properties_dict = element_dict.get("properties")    # dict
        return properties_dict


def user_input():       # Needs input validation
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