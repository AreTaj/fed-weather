"""
Aresh Tajvar, 2024
CS50 Python Final Project
Fed Weather

Unit Testing
Note: at least three functions need a related test
"""
#import pytest
from project import validate_station, station, api_and_parse, get_weather, format_and_print

def main():
    test_validate_station()
    test_station()
    test_api_and_parse()
    test_get_weather()
    test_format_and_print()

def test_validate_station():
    assert validate_station("KSEA") == "KSEA"
    assert validate_station("KBOS") == "KBOS"
    assert validate_station("KLAX") == "KLAX"

def test_station():
    assert station("KSEA") == "KSEA" or "Seattle, Seattle-Tacoma International Airport"
    assert station("PAMR") == "PAMR" or "Anchorage, Merrill Field Airport"
    assert station("KLAX") == "KLAX" or "Los Angeles, Los Angeles International Airport"

def test_api_and_parse():
    result = api_and_parse("KSEA")
    assert "temperature" in result

    result = api_and_parse("PAMR")
    assert "temperature" in result

"""
def test_get_weather():
    #result = get_weather(api_and_parse("KSEA"))
    #assert "temperature" and "qualityControl" in result
    ...

def test_format_and_print():
    # result: Temperature 
    # selection_data: {'unitCode': 'wmoUnit:degC', 'value': -8.9, 'qualityControl': 'V'}
    #test_result = format_and_print("Temperature", "{'unitCode': 'wmoUnit:degC', 'value': -8.9, 'qualityControl': 'V'}")
    #assert format_and_print("Temperature", "{'unitCode': 'wmoUnit:degC', 'value': -8.9, 'qualityControl': 'V'}") == "Temperature: -8.9 degC"
    ...
"""
    
if __name__ == "__main__":
    main()