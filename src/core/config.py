import os
from datetime import datetime
from dotenv import load_dotenv
from types import SimpleNamespace

load_dotenv()
if os.getenv("DB_URL"):
    db_url = os.getenv("DB_URL")
    db_string = db_url
else:
    db_type = os.getenv("DB_TYPE")
    db_user = os.getenv("DB_USER")
    db_name = os.getenv("DB_NAME")
    db_string = f"dbname={db_name} user={db_user}"

    if os.getenv("DB_PASSWORD"):
        db_pass = os.getenv("DB_PASSWORD")
        db_string += f" password={db_pass}"

db_string = db_string

DEFAULT_CITY = "Tampere"
DATE_FORMAT = "%d.%m.%Y"
DEFAULT_DAY = datetime.now().strftime(DATE_FORMAT)

SUPPORTED_LANGS = ['en', 'fi']
# configuration for webscraper
# Restaurant list on each cities
tampere = [
    {
        "areaName": "Hervanta",
        "restaurants": {
            "juvenes": {"Newton": "6",
                        "Konehuone": "6"},
            "compass": {"Reaktori": "0812"},
            "sodexo": {"Hertsi": "111"}
        }
    },
    {
        "areaName": "Keskusta",
        "restaurants": {
            "juvenes": {
                "Alakuppila": "13",
                "Yliopiston Ravintola": "13",
                "YR Yläkuppila": "13",
                "YR Fusion Kitchen": "13",
                "Rata": "72",
                "Frenckell": "33"
            },
            "compass": {"Minerva": "0815"},
            "sodexo": {"Linna": "116"}
        }
    },
    {
        "areaName": "TAYS",
        "restaurants": {
            "juvenes": {"Arvo": "5"},
            "compass": {"Reaktori": "0812", "Minerva": "0815"},
            "sodexo": {"Linna": "116", "Hertsi": "111"}
        }
    }
]

helsinki = [
    {
        "areaName": "Keskusta",
        "restaurants": {
            "sodexo": {
                "HY-Päärakennus": "1045996"
            }
        }
    },
    {
        "areaName": "Otaniemi",
        "restaurants": {
            "compass": {
                "A-Bloc": "3087",
                "TUAS": "0199",
                "Alvari": "0190",
                "Dipoli": "3101"
            }
        }
    },
    {
        "areaName": "Töölö",
        "restaurants": {
            "compass": {
                "Töölö-37": "3704",
                "Hanken": "3406",
                "Tempo": "1252"
            }
        }
    },
    {
        "areaName": "Arabia & Kumpula",
        "restaurants": {
            "compass": {"Arcada": "3003"}
        }
    },
    {
        "areaName": "Itä-Helsinki",
        "restaurants": {
            "compass": {"Opetustalo": "0083"},
            "sodexo": {"Myllypuro": "158"}
        }
    },
    {
        "areaName": "Viikki",
        "restaurants": {
            "sodexo": {"Ladonlukko": "68"}
        }
    },
]

# helsinki = {"compass": {
#     "3208": "Metropolia"},
#
# }
turku = [
    {
        "areaName": "TYS Nummenranta",
        "restaurants": {
            "juvenes": {"Block": "71",
                        "Block Fusion": "71"},
        }
    },
    {
        "areaName": "Turku-AMK",
        "restaurants": {
            "sodexo": {"Turku-AMK": "160"}
        }
    }
]


CITIES = [("Tampere", tampere),
          ("Helsinki", helsinki),
          ("Turku", turku)]

URLS = {"juvenes":
        "https://fi.jamix.cloud/apps/menuservice/rest/haku/menu/93077/{id}?lang={lang}",
        "compass":
        "https://www.compass-group.fi/menuapi/feed/json?costNumber={id}&language={lang}",
        "sodexo": "https://www.sodexo.fi{lang}ruokalistat/output/weekly_json/{id}"}
