import jq
import re
import logging

from dataclasses import asdict

from webscraper.models import unified_json
from webscraper import utils

logger = logging.getLogger(__name__)


def transform_response(restaurant_name, area_name, parsed_response):
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
    restaurant_dict = unified_json.UnifiedJson(
        restaurant_name, area_name, menu_options)
    return asdict(restaurant_dict)


def parse_response(restaurant_name, area_name, lang, response_json):
    """Parse JSON response from Compass Group.
    Params:
        id: Restaurant id to be queried into API.
        area_name: Area that the restaurant belongs to.
        response_json: A JSON response from Compass Group.

    Returns:
        parsed_json: A parsed JSON object hat follows the JsonTransform
        specification.
    """
    simplified_resp = jq.compile('''
        del(. | .PriceHeader,
            (.MenusForDays[].SetMenus[].SortOrder))
    ''').input_value(response_json).all()
    simplified_resp = simplified_resp[0]
    simplified_resp['lang'] = lang

    formatted_response = transform_response(
        restaurant_name, area_name, simplified_resp)
    return [formatted_response]
