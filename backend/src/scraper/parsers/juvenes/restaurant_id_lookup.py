# Lookup table for restaurants in Juvenes.

# Context: In some cases, Juvenes stack a lot of restaurants into the same json
# response, especially restaurants that are close together but known by the
# streets as different restaurants. So this lookup table/dictionary is to ease
# the pain points when parsing those restaurants.

# might be an inspiration for other restaurant chains.

RESTAURANT_UNIQUE_IDS = {
    # Tampere Herwanta
    "Newton": [56, 110],
    "Konehuone": [112],

    # Tampere Keskusta
    "Alakuppila": [7],
    "Yliopiston Ravintola": [56],
    "YR Yläkuppila": [120],
    "YR Fusion Kitchen": [22],

    # Tampere TAYS
    "Arvo": [56],
    "Arvo Cafe Lea": [22],

    # Tampere Keskusta (outside)
    "Rata": [56],
    "Frenckell": [56],

    # TAMK
    "Campusravita": [1],

    # Turku TYS
    "Block": [56],
    "Block Fusion": [22]

}
