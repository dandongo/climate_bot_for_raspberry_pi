import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
    TOKEN = os.environ.get('TOKEN')
    CHAT_ID = os.environ.get('CHAT_ID')
    LAT = os.environ.get('LAT')
    LNG = os.environ.get('LNG')
    # adjustable configurations
    # name the sensor
    SENSOR_ID = os.environ.get('SENSOR_ID') or "dht11_01"
    # define absolute directory for the log file
    LOG_FILE = os.environ.get('LOG_FILE') or "/home/ubuntu/git/climate/hyg_log.json"
    # emoji codes
    EMOJI_LOW_TEMPERATURE = os.environ.get('EMOJI_LOW_TEMPERATURE') or "\U0001F976"
    EMOJI_HIGH_TEMPERATURE = os.environ.get('EMOJI_HIGH_TEMPERATURE') or "\U0001F975"
    EMOJI_LOW_HUMIDITY = os.environ.get('EMOJI_LOW_HUMIDITY') or "\U0001F335"
    EMOJI_HIGH_HUMIDITY = os.environ.get('EMOJI_HIGH_HUMIDITY') or "\U0001F4A6"
    
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
