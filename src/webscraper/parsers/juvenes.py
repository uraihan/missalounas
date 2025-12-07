import jq
import jsonschema

# from .base import Restaurant
from datetime import datetime
from pprint import pformat
from dataclasses import asdict
from collections import defaultdict

from webscraper import utils
from webscraper.models import juvenes_response
from webscraper.models import unified_json

# RESTAURANT_NAMES = {"22": "Arvo Cafe Lea",
#                     "56": "Arvo",
#                     "7": "Alakuppila",
#                     "27": "YR Henkilöstolounas",
#                     "56": "Yliopiston Ravintola",
#                     "120": "YR Yläkuppila",
#                     "22": "YR Fusion",
#                     "56": "Newton",
#                     "110": "Newton",
#                     "112": "Cafe Konehuone"}

# class Juvenes(Restaurant):


def get_restaurant_data(response_json):
    """Get restaurant data from raw JSON response.
    Params:
        response_json: Raw JSON response from the API

    Returns:
        restaurant_data: Trimmed down version of the JSON response.
    """
    restaurant_data = []
    simplified_resp = jq.compile('''
        [.[].menuTypes[] | {menuTypeName: .menuTypeName} + .menus[]]
        | del(.[] | .menuTypeId, .menuId, .menuAdditionalName,
              .menuName,
              (.days[]| .weekday, .lang),
              (.days[].mealoptions[] | .orderNumber),
              (.days[].mealoptions[].menuItems[] | .orderNumber,
               .portionSize, .images))
        | .[]
    ''').input_value(response_json).all()

    for item in simplified_resp:
        if item['menuTypeName'] == 'Ateriapalvelut koulu':
            continue
        else:
            for day in item['days']:
                response_format = "%Y%m%d"
                # probably can refactor this (or separate as a model
                # module)
                # date_format = internal_json.DATE_FORMAT
                # datetime_fmt = datetime.strptime(
                #     str(day['date']), response_format)
                # datetime_fmt = f"{datetime_fmt.strftime(date_format)}"
                day['date'] = utils.format_date(day['date'],
                                                response_format)
            restaurant_data.append(item)

    return restaurant_data
    # maybe we can use generator function here?


def check_restaurant_name(id, menu_type):
    # Simplify this a bit better
    restaurant_name = menu_type
    if restaurant_name == "Lounas":
        if id == "6":
            restaurant_name = "Newton"
        if id == "13":
            restaurant_name = "Yliopiston Ravintola"
        if id == "5":
            restaurant_name = "Arvo"
        if id == "72":
            restaurant_name = "Rata"
        if id == "33":
            restaurant_name = "Frenckell"

    if restaurant_name == "Kasvis":
        if id == "6":
            restaurant_name = "Newton"

    if restaurant_name == "Fusion kitchen":
        if id == "5":
            restaurant_name = "Arvo"
        if id == "13":
            restaurant_name = "YR Fusion Kitchen"

    return restaurant_name


def parse_response(id, lang, response_json):
    """Parse JSON response from Juvenes.
    Params:
        response_json: A JSON response from Juvenes.

    Returns:
        parsed_json: A parsed JSON object hat follows the JsonTransform
        specification.
    """

    # for debug purpose, use a test json file
    # response_json = json.load(open("ravintola-newton-6.json"))

    try:
        # Validate response
        jsonschema.validate(response_json, schema=juvenes_response.SCHEMA)
        print("200: JSON Data is valid!")

        restaurant_data = get_restaurant_data(response_json)

        # with open('oneline_response.txt', 'w') as f:
        #     f.write(str(restaurant_data[0]))
        # breakpoint()

    except jsonschema.exceptions.ValidationError as e:
        print(f"500: Response error. {e.message}")

    parsed_json = []
    for x in restaurant_data:
        menu_type = x['menuTypeName']
        restaurant_name = check_restaurant_name(id, menu_type)
        food_list = []

        for day in x['days']:
            date = day['date']
            # lang = day['lang']
            for option in day['mealoptions']:
                menu_type_id = option['id']
                for item in option['menuItems']:
                    food_name = item['name']
                    diets = item['diets']
                    food_item = unified_json.IndividualMenu(
                        food_name, diets, date, menu_type, menu_type_id, lang)
                    food_list.append(food_item)

        restaurant_object = unified_json.UnifiedJson(
            restaurant_name, food_list)
        parsed_json.append(asdict(restaurant_object))

    parsed_json = utils.combine_restaurants(parsed_json)
    return parsed_json
    # with open('response.txt', 'w') as f:
    #     f.write(pformat(restaurant_data, width=140))
