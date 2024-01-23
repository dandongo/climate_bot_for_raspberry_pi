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
from config import Config

# global variables
# time between readings
interval = 60
# name the sensor
sensor_id = "dht11_01"
# define absolute directory for the log file
log_file = "/home/ubuntu/git/climate/hyg_log.json"
#telegram stuff
TOKEN = "6536298415:AAH81I-gqKTVFhM5e_Z8_fXI3Bma1UhZGXg"
CHAT_ID = "811059940"
# emoji codes
emoji_low_temperature = "\U0001F976"
emoji_high_temperature = "\U0001F975"
emoji_low_humidity = "\U0001F335"
emoji_high_humidity = "\U0001F4A6"


# best climate practices (bcp) dictionary, temp values in C
bcp = {
    "seedling" : {
        "temperature": {
            "day" : {
                    "minimum" : 21,
                    "maximum" : 29,
            },
            "night" : {
                    "minimum" : 18,
                    "maximum" : 27,
            }
        },
        "humidity" : {
            "minimum" : 75,
            "maximum" : 85
        }
    },
    "vegetation" : {
        "temperature": {
            "day" : {
                    "minimum" : 21,
                    "maximum" : 29,
            },
            "night" : {
                    "minimum" : 16,
                    "maximum" : 24,
            },
        },
        "humidity" : {
            "minimum" : 45,
            "maximum" : 55
        },
    },
    "flowering" : {
        "temperature": {
            "day" : {
                    "minimum" : 21,
                    "maximum" : 29,
            },
            "night" : {
                    "minimum" : 16,
                    "maximum" : 24,
            },
        },
        "humidity" : {
            "minimum" : 35,
            "maximum" : 45
        }
    }
}

# define what stage the plant is in (you should move this to another file you can easily change perhaps even in the web browser)
stage = "seedling"
#stage = "vegetation"
#stage = "flowering"

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
sensor = adafruit_dht.DHT11(board.D23)

def take_reading():
    try:
        # take sensor readings
        humidity = sensor.humidity
        temp = sensor.temperature
        temp_f = temp * 9 / 5 + 32
        # for testing, decomment to override sensor readings to -- for example -- trigger the corresponding alarm
        #temp = 90
        #humidity = 5
        #check readings for values out of range
        day_night = "day"
        try:
            day_night = day_or_night()
        except:
            print("could not determine if day or night, using day")
        if temp < bcp[stage]["temperature"][day_night]["minimum"]:
            print("temperature is too low for " + day_night)
            message_title = emoji_low_temperature + emoji_low_temperature + emoji_low_temperature + \
                "LOW Temperature Alert! " + emoji_low_temperature + emoji_low_temperature + \
                emoji_low_temperature + "\nRecorded " + str(temp) + "C (mininum for " + stage + " is set to " + \
                str(bcp[stage]["temperature"][day_night]["minimum"]) + "C)"
            send_text = "https://api.telegram.org/bot" + TOKEN + "/sendMessage?chat_id=" + CHAT_ID + "&parse_mode=Markdown&text=" + message_title
            requests.get(send_text)
        if temp > bcp[stage]["temperature"][day_night]["maximum"]:
            print("temperature is too high for " + day_night)
            message_title = emoji_high_temperature + emoji_high_temperature + emoji_high_temperature + \
                "HIGH Temperature Alert! " + emoji_high_temperature + emoji_high_temperature + \
                emoji_high_temperature + "\nRecorded " + str(temp) + "C (maximum for " + stage + " is set to " + \
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


        # get time
        ts = str(time.time())


        # consolidate readings and time
        reading = json.dumps(
            {
                'sensor_id':sensor_id,
                'time':ts,
                'readings':
                {
                    'temp':temp,
                    'temp_f':temp_f,
                    'humidity':humidity
                }
            }
        )
        print(reading)

        try:
            try:
                with open(log_file, "x") as f:
                    f.write(reading)
            except:
                with open(log_file, "a") as f:
                    f.write(reading)
            f.close
        except:
            print("could not write to log")
    except RuntimeError as error:
        print(error.args[0])
    except Exception as error:
        sensor.exit()
        raise error

take_reading()