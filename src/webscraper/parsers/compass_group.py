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
                                                        menu_type=menu_type,
                                                        date=date,
                                                        menu_uid=menu_type_id,
                                                        lang=lang)
                menu_options.append(menu_item)

    restaurant_dict = unified_json.RestaurantContainer(
        restaurant_name, area_name, menu_options)
    return asdict(restaurant_dict)


def parse_response(restaurant_name, area_name, lang, response_json):
    """Parse JSON response from Compass Group.
    Params:
        restaurant_name: Name of the restaurant to be queried from API.
        area_name: Area that the restaurant belongs to.
        response_json: A JSON response from Compass Group.

    Returns:
        parsed_json: A parsed JSON object hat follows the JsonTransform
        specification.
    """
    try:
        simplified_resp = jq.compile('''
            del(. | .PriceHeader,
                (.MenusForDays[].SetMenus[].SortOrder))
        ''').input_value(response_json).all()
    except ValueError as e:
        logger.warning(f"""{e}.
            Restaurant {restaurant_name} either has no JSON for language
            {lang} or got an unexpected JSON response
        """)
        logger.warning(f"Passing default formatted response for restaurant {
                       restaurant_name}")

        return [utils.create_empty_item(restaurant_name, area_name, lang)]

    simplified_resp = simplified_resp[0]
    simplified_resp['lang'] = lang

    formatted_response = transform_response(
        restaurant_name, area_name, simplified_resp)
    return [formatted_response]
