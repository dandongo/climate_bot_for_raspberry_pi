import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
    TOKEN = os.environ.get('TOKEN')
    CHAT_ID = os.environ.get('CHAT_ID')
    lat = os.environ.get('lat')
    lng = os.environ.get('lng')
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
