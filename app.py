#!/usr/bin/python

import adafruit_dht
import board
import psutil
import time
from time import sleep
import json
import os
import requests
import argparse
from day_or_night import day_or_night
from dotenv import load_dotenv
import config

# bring in the configuration file
config_obj = config.Config()

# global variables
# name the sensor
sensor_id = config_obj.SENSOR_ID
# define absolute directory for the readings file
readings_file = config_obj.READINGS_FILE
#telegram stuff
TOKEN = config_obj.TOKEN
CHAT_ID = config_obj.CHAT_ID
# emoji codes
emoji_low_temperature = config_obj.EMOJI_LOW_TEMPERATURE
emoji_high_temperature = config_obj.EMOJI_HIGH_TEMPERATURE
emoji_low_humidity = config_obj.EMOJI_LOW_HUMIDITY
emoji_high_humidity = config_obj.EMOJI_HIGH_HUMIDITY
# best climate practices (bcp) dictionary
bcp = config_obj.BCP
# stage as set in config
stage = config_obj.STAGE

# initiate argument parser
parser = argparse.ArgumentParser(description="This script measures humidity and temperature and sends a telegram message, when temp and/or humidity are out of range as set in the global variables section.")
# add long an short argument
parser.add_argument("-i", "--intervall", help="interval in which measurement is performed", type=int)
# read arguments from the command line
args = parser.parse_args()

# We first check if a libgpiod process is running. If yes, we kill it!
for proc in psutil.process_iter():
    if proc.name() == 'libgpiod_pulsein' or proc.name() == 'libgpiod_pulsei':
        proc.kill()

def take_reading():
    sensor = adafruit_dht.DHT11(board.D23)
    # take sensor readings
    humidity = sensor.humidity
    temperature = sensor.temperature
    # for testing, decomment to override sensor readings to -- for example -- trigger the corresponding alarm
    #temperature = 90
    #humidity = 5
    #check readings for values out of range
    day_night = "day"
    try:
        day_night = day_or_night()
    except:
        print("could not determine if day or night, using day")
    if temperature < bcp[stage]["temperature"][day_night]["minimum"]:
        print("temperature is too low for " + day_night)
        message_title = emoji_low_temperature + emoji_low_temperature + emoji_low_temperature + \
            "LOW Temperature Alert! " + emoji_low_temperature + emoji_low_temperature + \
            emoji_low_temperature + "\nRecorded " + str(temperature) + "C (mininum for " + stage + " is set to " + \
            str(bcp[stage]["temperature"][day_night]["minimum"]) + "C)"
        send_text = "https://api.telegram.org/bot" + TOKEN + "/sendMessage?chat_id=" + CHAT_ID + "&parse_mode=Markdown&text=" + message_title
        requests.get(send_text)
    if temperature > bcp[stage]["temperature"][day_night]["maximum"]:
        print("temperature is too high for " + day_night)
        message_title = emoji_high_temperature + emoji_high_temperature + emoji_high_temperature + \
            "HIGH Temperature Alert! " + emoji_high_temperature + emoji_high_temperature + \
            emoji_high_temperature + "\nRecorded " + str(temperature) + "C (maximum for " + stage + " is set to " + \
            str(bcp[stage]["temperature"][day_night]["maximum"]) + "C)"
        send_text = "https://api.telegram.org/bot" + TOKEN + "/sendMessage?chat_id=" + CHAT_ID + "&parse_mode=Markdown&text=" + message_title
        requests.get(send_text)
    if humidity < bcp[stage]["humidity"]["minimum"]:
        print("humidity is too low")
        message_title = emoji_low_humidity + emoji_low_humidity + emoji_low_humidity + \
            "LOW Humidity Alert! " + emoji_low_humidity + emoji_low_humidity + \
            emoji_low_humidity + "\nRecorded " + str(humidity) + " (mininum for " + stage + " is set to " + \
            str(bcp[stage]["humidity"]["minimum"]) + ")"
        send_text = "https://api.telegram.org/bot" + TOKEN + "/sendMessage?chat_id=" + CHAT_ID + "&parse_mode=Markdown&text=" + message_title
        requests.get(send_text)
    if humidity > bcp[stage]["humidity"]["maximum"]:
        print("humidity is too high")
        message_title = emoji_high_humidity + emoji_high_humidity + emoji_high_humidity + \
            "HIGH Humidity Alert! " + emoji_high_humidity + emoji_high_humidity + \
            emoji_high_humidity + "\nRecorded " + str(humidity) + " (mininum for " + stage + " is set to " + \
            str(bcp[stage]["humidity"]["maximum"]) + ")"
        send_text = "https://api.telegram.org/bot" + TOKEN + "/sendMessage?chat_id=" + CHAT_ID + "&parse_mode=Markdown&text=" + message_title
        requests.get(send_text)

    # get timestamp
    ts = str(time.time())
    
    # create the reading to append to the json
    reading = {
        "timestamp" : ts,
        "readings" : {
            "temperature" : temperature,
            "humidity" : humidity 
        }
    }

    try:
        if os.path.exists(readings_file):
            print("readings file exists! " + readings_file)
            with open(readings_file, 'r') as f:
                data = json.load(f)
        else:
            print("file doesn't exist! " + readings_file)
            data = {sensor_id}
        print(reading)
        
        data[sensor_id].append(reading)
#        with open(readings_file, 'w') as f:
#            json.dump(data, f, indent=4)

    except:
        print("WARNING: Could not write readings to file!")

try:
    take_reading()
except RuntimeError as error:
    print(error.args[0])
except Exception as error:
    sensor.exit()
    raise error
