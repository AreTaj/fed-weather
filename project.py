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
  if valid input
       return selected weather detail(s)
  elif no input
       return some weather details from preselected list
  else
      ValueError
"""

# https://www.weather.gov/documentation/services-web-api#/
# https://api.weather.gov/stations/KCRQ/observations 

def main():
    weather()

def station():      # Need to include station input validation
    station = input("Input a weather station: ")
    return station

def weather():
    station_id = station()
    response = requests.get(f"https://api.weather.gov/stations/{station_id}/observations")
    all_data = response.json()                          # dict
    list_data = all_data["features"]                    # list
    element_data = list_data[0]                         # dict
    properties_data = element_data.get("properties")    # dict

    selection = input("Weather property: ")
    selection_data = properties_data.get(selection)     # dict
    # Below two lines are to format selection for readability. Ex: barometricPressure --> Barometric pressure, temperature --> Temperature
    s = selection
    result = "".join(' ' + i if i.isupper() else i for i in s).capitalize()

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