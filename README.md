# Fed Weather
#### Video Demo:  <https://youtu.be/mugxMettZuQ>
#### Description: 
Aresh Tajvar, 2024
CS50 Python Final Project
Fed Weather

Github repository:
https://github.com/AreTaj/fed-weather

Harvard CS50 Python Final Project:
https://cs50.harvard.edu/python/2022/project/

NOAA NWS API Documentation:
https://www.weather.gov/documentation/services-web-api#/

NOAA NWS Station Observations API:
https://api.weather.gov/stations/{station}/observations 

This program is designed to access trustworthy and reliably-accessible weather data and report it in a user-friendly manner. To do so, it accesses the NOAA National Weather Service free and public-access API at https://api.weather.gov and is able to report a range of weather condition details from any K-series NWS station (ex: KLAX for Los Angeles). In order to write this program, I applied the skills I learned through the course of Harvard's CS50 Python course and learned more here and there on how to achieve specific functionality for my project. I used the requests library as well, which was not covered in CS50. Through the course of writing code for my project, I strove to follow best-practices and keep clean and thoroughly-commented code. I also aimed to keep my methods in line with the single responsibility principle where possible, which meant that I needed to break down methods more than I had initially planned. The result is a modular and functional program that is defensively programmed to prevent users from accidentally inducing errors.

The intended and tested behavior of each method and the overall program is as follows:

validate_station()
User was prompted in main() for weather station input; per NOAA convention, input must follow the standard for station code names (ex: KSEA for Seattle, WA). If an incorrect input is provided that does not follow the standard for station code names (four capital letters, verified through a regular expression match), then reprompt the user and suggest some valid sample inputs. If an input is provided that does meet the standard and also passes the regular expression check, then it will pass the provided input code to the API to verify that the station exists by checking the status code returned by the API; 200 indicates normal operation, 404 indicates station not found. For example, "KLAX" passes regex, exists in API database, and thus is valid. "FAIL" passes regex, but does not exist in API database, and thus is not valid. If the station does not exist in API database, the program will reprompt the user and suggest some valid sample inputs. However, if any API check returns any value other than 200 (normal operation) or 404 (station not found), this will indicate a connection issue or that the API is down, and the program will sys.exit quit and print the relevant error as there is no point in running the rest of the program without API access. If everything passes and the station input is validated, the station code will be passed to station() below. Two separate variables are used for unvalidated and validated station codes respectively to ensure an unvalidated and incorrect station code is not passed to the rest of the program.

station()
Take validated station code and pass to the API. The method parses through the JSON returned by API until it reaches the station_properties["name"], which provides the full name of the relevant NWS station. Return station name. For example, "KSEA" is the short code corresponding to "Seattle, Seattle-Tacoma International Airport", which is returned and printed by the program. The sole function of this method is to get, print, and return the full name of the station. This helps the user relate the four-letter code to a real location and also facilitates testing of the program; if "KBOS" does not return/print "Boston, Logan International Airport", then something is wrong.

api_and_parse()
Take validated station code and pass to API. Again, check the returned status code. If status is not 200 (normal), then kill the program; the station code has already been validated meaning there is no need to check for a 404 again, which indicates that there must have been a problem with the connection or the API. Then, program parses the JSON provided by the API until it reaches the dict of all available weather properties (temperature, dewpoint, windSpeed, etc). properties_dict is stored, returned, and passed to get_weather for further breakdown.

get_weather()
Take properties_dict, which contains all available weather properties and values. Then, prompt user for desired weather detail (ex: temperature, barometricPressure). The API can only take weather detail inputs that exactly match how they are named in API data, so the user must input exactly as "temperature", "barometricPressure", or "relativeHumidity". This is specified in the input prompt and a list of valid options is provided. If the user does not input something that is in the list of valid inputs, print "Invalid" and reprompt user. If user does input something that is in the list of valid inputs, then pull the selected data point out of properties_dict and begin formatting for printing readability. This will make "barometricPressure" become "Barometric pressure" or "temperature" become "Temperature". Method will return both the user's selected weather detail and the corresponding data from properties_dict, both of which are passed to format_and_print() for final output.

format_and_print()
Take result and selection_data from get_weather(). Note, the API returns information in this format: Temperature {'unitCode': 'wmoUnit:degC', 'value': 9}. format_and_print() splits that return into something more readable. The first part is the user's selected weather detail, in this case temperature. Next is unitCode, wmoUnit, and value; to summarize, this translate to a value of 9 with units in degrees Celsius. To properly convey this to user, split the string and keep the units and value ("degC" and "9"). Then, combine these with the user's selected weather detail. Finally, the method prints the selected weather detail in form "Temperature: 13.7 degC". This ends the program.

