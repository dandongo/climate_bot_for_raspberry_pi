import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
    # this/these are the values you are most likely to want to change
    # uncomment the stage your plants are in.
    STAGE = "seedling"
    #STAGE = "vegetation"
    #STAGE = "flowering"
    # name your sensor
    SENSOR_ID = "dht11_01"
    # emoji codes
    EMOJI_LOW_TEMPERATURE = "\U0001F976"
    EMOJI_HIGH_TEMPERATURE = "\U0001F975"
    EMOJI_LOW_HUMIDITY = "\U0001F335"
    EMOJI_HIGH_HUMIDITY = "\U0001F4A6"

    # these settings are imported from the private .env file.
    #     create a .env file with the below values 
    TOKEN = os.environ.get('TOKEN')
    CHAT_ID = os.environ.get('CHAT_ID')
    LAT = os.environ.get('LAT')
    LNG = os.environ.get('LNG')
    LOG_FILE = os.environ.get('LOG_FILE')
    
    # best climate practices (bcp) dictionary, temp values in C
    BCP = {
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
