import jq
import re
from pprint import pformat
from dataclasses import asdict

from webscraper.models import unified_json
from webscraper import utils


def transform_response(parsed_response):
    restaurant_name = parsed_response['RestaurantName']
    lang = parsed_response['lang']
    menu_options = []

    for item in parsed_response['MenusForDays']:
        date = item['Date']
        date_format = "%Y-%m-%dT%H:%M:%S%z"
        date = utils.format_date(date, date_format)
        # date needs to be formatted
        for idx, option in enumerate(item['SetMenus']):
            menu_type = option['Name']
            for food in option['Components']:
                food = re.split(r'\s+(?=\()', food)
                food_name = food[0]
                diets = food[1]
                menu_type_id = idx
                menu_item = unified_json.IndividualMenu(food_name,
                                                        diets,
                                                        date,
                                                        menu_type,
                                                        menu_type_id,
                                                        lang)
                menu_options.append(menu_item)
    restaurant_dict = unified_json.UnifiedJson(restaurant_name,
                                               menu_options)
    return asdict(restaurant_dict)


def parse_response(id, lang, response_json):
    simplified_resp = jq.compile('''
        del(. | .PriceHeader,
            (.MenusForDays[].SetMenus[].SortOrder))
    ''').input_value(response_json).all()
    simplified_resp = simplified_resp[0]
    simplified_resp['lang'] = lang

    formatted_response = transform_response(simplified_resp)
    return [formatted_response]

    with open('compass_formatted_response.txt', 'w') as f:
        f.write(pformat(formatted_response, width=140))


# for city in RAVINTOLAT:
#     parse_compass(city)
