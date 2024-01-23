#!/usr/bin/python

import time
import requests
import json
from colorama import Fore, Style

def day_or_night():
    # Replace these values with your location's latitude and longitude
    lat = 36.587222
    lng = -79.404444
    # Get the current date in YYYY-MM-DD format
    date = time.strftime("%Y-%m-%d")
    # Construct the API URL with the parameters
    url = f"https://api.sunrise-sunset.org/json?lat={lat}&lng={lng}&date={date}&formatted=0"
    # Send a GET request to the API and get the response
    response = requests.get(url)
    # Check if the response is successful
    if response.status_code == 200:
        # Parse the JSON data from the response
        data = json.loads(response.text)
        # Extract the sunrise and sunset times in UTC
        sunrise = data["results"]["sunrise"]
        sunset = data["results"]["sunset"]
        # Convert the times to local time zone
        sunrise_local = time.strptime(sunrise, "%Y-%m-%dT%H:%M:%S%z")
        sunset_local = time.strptime(sunset, "%Y-%m-%dT%H:%M:%S%z")
        # Get the current time in local time zone
        now_local = time.localtime()
        # Compare the current time with the sunrise and sunset times
        if now_local < sunrise_local or now_local > sunset_local:
            return "night"
        else:
            return "day"
    else:
        # Handle the error
        print('Something went wrong')