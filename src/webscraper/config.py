# configuration for webscraper
SUPPORTED_LANGS = ['en', 'fi']
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
            "juvenes": {"Alakuppila": "13",
                        "Yliopiston Ravintola": "13",
                        "YR Yläkuppila": "13",
                        "YR Fusion Kitchen": "13",
                        "Rata": "72",
                        "Frenckell": "33"},
            "compass": {"Minerva": "0815"},
            "sodexo": {"Linna": "116"}
        }
    },
    {
        "areaName": "TAYS",
        "restaurants": {
            "juvenes": {"Arvo": "5",
                        "Arvo Cafe Lea": "5"},
        }
    },
    {
        "areaName": "TAMK",
        "restaurants": {
            "campusravita": {"Campusravita": "1"}
        }
    }
]

helsinki = [
    {
        "areaName": "Espoo",
        "restaurants": {
            "compass": {"Metropolia": "3208"}
        }
    },
    {
        "areaName": "Kallio",
        "restaurants": {
            "compass": {"Kookos": "3067"}
        }
    },
    {
        "areaName": "Keskusta",
        "restaurants": {
            "sodexo": {
                "HY-Päärakennus": "1045996",
                "Musiikkitalo Klubi": "3100"
            }
        }
    },
    {
        "areaName": "Otaniemi",
        "restaurants": {
            "compass": {"A-Bloc": "3087",
                        "TUAS": "0199",
                        "Alvari": "0190",
                        "Dipoli": "3101",
                        "Laurea Otaniemen Kampus": "3292"},
            "sodexo": {"Kvarkki": "86",
                       "Tietotekniikantalo": "6754"}
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
            "compass": {
                "Arcada": "3003",
                "DIAK-Kalasatama": "3104",
                "Luova": "1251"
            }
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
    {
        "areaName": "Vantaa",
        "restaurants": {
            "compass": {"Laurea Tikkurilan kampus": "3032"},
            "sodexo": {"Metropolia Myyrmäki": "152"}
        }
    }
]

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

URLS = {
    "juvenes": "https://fi.jamix.cloud/apps/menuservice/rest/haku/menu/93077/{id}?lang={lang}",
    "compass": "https://www.compass-group.fi/menuapi/feed/json?costNumber={id}&language={lang}",
    "sodexo": "https://www.sodexo.fi{lang}ruokalistat/output/weekly_json/{id}",
    "campusravita":
    "https://fi.jamix.cloud/apps/menuservice/rest/haku/menu/97603/{id}?lang={lang}"
}
