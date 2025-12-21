# configuration for webscraper
SUPPORTED_LANGS = ["en", "fi"]
# Restaurant list on each cities
tampere = [
    {
        "areaName": "Hervanta",
        "restaurants": {
            "juvenes": {"Newton": "6", "Konehuone": "6"},
            "compass": {"Reaktori": "0812"},
            "sodexo": {"Hertsi": "111"},
        },
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
                "Frenckell": "33",
            },
            "compass": {"Minerva": "0815"},
            "sodexo": {"Linna": "116"},
        },
    },
    {
        "areaName": "TAYS",
        "restaurants": {
            "juvenes": {"Arvo": "5", "Arvo Cafe Lea": "5"},
        },
    },
    {"areaName": "TAMK", "restaurants": {"campusravita": {"Campusravita": "1"}}},
]

helsinki = [
    {"areaName": "Espoo", "restaurants": {"compass": {"Metropolia": "3208"}}},
    {"areaName": "Kallio", "restaurants": {"compass": {"Kookos": "3067"}}},
    {
        "areaName": "Keskusta",
        "restaurants": {
            "sodexo": {"HY-Päärakennus": "1045996", "Musiikkitalo Klubi": "3100"},
            "unicafe": {
                "Kaivopiha": ["2558", "2543"],
                "Kaisa-talo": ["4383", "1375"],
                "Metsätalo": ["2583", "1359"],
                "Myohä Cafe & Bar": ["4379", "4377"],
                "Olivia": ["2510", "1360"],
                "Porthania": ["2514", "1364"],
                "Rotunda": ["2585", "1370"],
                "Soc&Kom": ["2511", "1372"],
                "Topelias": ["2696", "1362"],
            },
        },
    },
    {
        "areaName": "Otaniemi",
        "restaurants": {
            "compass": {
                "A-Bloc": "3087",
                "TUAS": "0199",
                "Alvari": "0190",
                "Dipoli": "3101",
                "Laurea Otaniemen Kampus": "3292",
            },
            "sodexo": {"Kvarkki": "86", "Tietotekniikantalo": "6754"},
        },
    },
    {
        "areaName": "Töölö",
        "restaurants": {
            "compass": {"Töölö-37": "3704", "Hanken": "3406", "Tempo": "1252"},
            "unicafe": {"Serpens": ["5393", "5391"]},
        },
    },
    {
        "areaName": "Arabia & Kumpula",
        "restaurants": {
            "compass": {"Arcada": "3003", "DIAK-Kalasatama": "3104", "Luova": "1251"},
            "unicafe": {
                "Chemicum": ["2498", "1354"],
                "Exactum": ["2500", "1356"],
                "Physicum": ["2591", "1363"],
            },
        },
    },
    {
        "areaName": "Itä-Helsinki",
        "restaurants": {
            "compass": {"Opetustalo": "0083"},
            "sodexo": {"Myllypuro": "158"},
        },
    },
    {
        "areaName": "Viikki",
        "restaurants": {
            "sodexo": {"Ladonlukko": "68"},
            "unicafe": {
                "Biokeskus": ["2501", "1335"],
                "Biokeskus 2": ["4575", "4573"],
                "Infokeskus (Student/alakerta)": ["4518", "4516"],
                "Tahka": ["4577", "4576"],
                "Viikuna": ["2589", "1374"],
            },
        },
    },
    {
        "areaName": "Vantaa",
        "restaurants": {
            "compass": {"Laurea Tikkurilan kampus": "3032"},
            "sodexo": {"Metropolia Myyrmäki": "152"},
        },
    },
    {
        "areaName": "Meilahti",
        "restaurants": {
            "unicafe": {"Meilahti": ["2508", "1358"], "Terkko": ["5225", "5223"]}
        },
    },
]

turku = [
    {
        "areaName": "TYS Nummenranta",
        "restaurants": {
            "juvenes": {"Block": "71", "Block Fusion": "71"},
        },
    },
    {"areaName": "Turku-AMK", "restaurants": {"sodexo": {"Turku-AMK": "160"}}},
    {
        "areaName": "UTU Kampus",
        "restaurants": {
            "unica": {
                "Assarin-Ulakko": "1920",
                "Macciavelli": "1970",
                "Galilei": "1995",
                "Monttu ja Mercatori": "1940",
            }
        },
    },
    {
        "areaName": "Kupittaan kampus",
        "restaurants": {
            "unica": {
                "Dental": "1980",
                "Linus": "2000",
                "Kisälli": "1900",
                "Delica": "1985",
                "Deli Pharma": "198501",
            }
        },
    },
    {"areaName": "Taidekampus", "restaurants": {"unica": {"Sigyn": "1965"}}},
    {"areaName": "Keskusta", "restaurants": {"unica": {"Unican Kulma": "1990"}}},
]


CITIES = [("Tampere", tampere), ("Helsinki", helsinki), ("Turku", turku)]

URLS = {
    "juvenes": "https://fi.jamix.cloud/apps/menuservice/rest/haku/menu/93077/{id}?lang={lang}",
    "compass": "https://www.compass-group.fi/menuapi/feed/json?costNumber={id}&language={lang}",
    "sodexo": "https://www.sodexo.fi{lang}ruokalistat/output/weekly_json/{id}",
    "campusravita": "https://fi.jamix.cloud/apps/menuservice/rest/haku/menu/97603/{id}?lang={lang}",
    "unicafe": "https://unicafe.fi/wp-json/swiss/v1/restaurants/?lang={lang}",
    "unica": "https://www.unica.fi/menuapi/feed/json?costNumber={id}&language={lang}",
}
