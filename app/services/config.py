# Restaurant list on each cities
tampere = {"juvenes": {
    "6": "Newton",
    "13": "keskusta",
    "5": "Arvo",
    "72": "Rata",
    "33": "Frenckell"},
    "compass": {"0812": "Reaktori", "0815": "Minerva"},
    "sodexo": {"116": "Linna", "111": "Hertsi"}
}
helsinki = {"compass": {
    "3087": "A-Bloc",
    "3704": "Töölö-37",
    "0199": "TUAS",
    "0190": "Alvari",
    "3003": "Arcada",
    "0083": "Opetustalo",
    "3101": "Dipoli",
    "3208": "Metropolia"},

    # "sodexo": {
    # "1045996": "HY-Päärakennus",
    # "68": "Ladonlukko",
    # "158": "Myllypuro"}
}
turku = {"juvenes": {"71": "Block"},
         "sodexo": {"160": "Turun-AMK"}
         }
# session = requests.Session()
# headers = {'Cache-Control': 'no-cache'}
SUPPORTED_LANGS = ['en', 'fi']

CITIES = [("Tampere", tampere), ("Helsinki", helsinki)]
URLS = {"juvenes":
        "https://fi.jamix.cloud/apps/menuservice/rest/haku/menu/93077/{id}?lang={lang}",
        "compass":
        "https://www.compass-group.fi/menuapi/feed/json?costNumber={id}&language={lang}",
        "sodexo": "https://www.sodexo.fi{lang}ruokalistat/output/weekly_json/{id}"}
