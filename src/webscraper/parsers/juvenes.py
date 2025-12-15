import jq
import jsonschema
import logging

from dataclasses import asdict
from types import SimpleNamespace
from itertools import chain

from webscraper import utils
from webscraper.models import juvenes_response, unified_json
from webscraper.models.juvenes_lookup import RESTAURANT_UNIQUE_IDS

logger = logging.getLogger(__name__)


def get_essential_chunk(response, sub_rest_id):
    response_object = SimpleNamespace(response[0])
    result = []
    for id in sub_rest_id:
        for menu_type in response_object.menuTypes:
            if menu_type.get('menuTypeId') == id:
                result.append(menu_type)

    return result


def get_restaurant_data(restaurant_name, response_json):
    """Get the relevant restaurant data from raw JSON response.
    Params:
        restaurant_name: Name of restaurant associated with the provided
            response_json.
        response_json: Raw JSON response from the API

    Returns:
        restaurant_data: Trimmed down version of the JSON response.
    """
    sub_restaurant_id = RESTAURANT_UNIQUE_IDS.get(restaurant_name)
    essential_chunk = get_essential_chunk(response_json, sub_restaurant_id)
    simplified_resp = jq.compile('''
        del(.[].menus[] | .menuId, .menuAdditionalName, .menuName,
              (.days[] | .weekday, .lang),
              (.days[].mealoptions[] | .id),
              (.days[].mealoptions[].menuItems[] | .orderNumber,
               .portionSize, .images))
        | map(.menus = [.menus[] | . + .days[] | del(.days)])
        | map(.restaurantUniqueId = .menuTypeId | del(.menuTypeId))
        | .[]
    ''').input_value(essential_chunk).all()

    restaurant_data = []
    for item in simplified_resp:
        for menu in item['menus']:
            response_format = "%Y%m%d"
            menu['date'] = utils.format_date(menu['date'],
                                             response_format)
        restaurant_data.append(item)

    return restaurant_data
    # maybe we can use generator function here?


def get_unified_menu(menu_option, menu_item, day, lang):
    """Form a unified menu container.
    """
    food_list = unified_json.IndividualMenu(
        food_name=menu_item.get('name'),
        diets=menu_item.get('diets'),
        menu_type=menu_option.get('name'),
        date=day.get('date'),
        menu_uid=menu_option.get('orderNumber'),
        lang=lang)

    return food_list


def parse_response(restaurant_name, area_name, lang, response_json):
    """Parse JSON response from Juvenes.
    Params:
        restaurant_name: Name of the restaurant to be queried from API.
        restaurant_name: Name of restaurant to be parsed.
        area_name: Area that the restaurant belongs to.
        response_json: A JSON response from Juvenes.

    Returns:
        parsed_json: A parsed JSON object hat follows the JsonTransform
        specification.
    """

    # for debug purpose, use a test json file

    try:
        # Validate response (could be replaced by pydantic?)
        jsonschema.validate(response_json, schema=juvenes_response.SCHEMA)

        # with open('oneline_response.txt', 'w') as f:
        #     f.write(str(restaurant_data[0]))
        # breakpoint()

    except jsonschema.exceptions.ValidationError as e:
        logger.error(f"JSON data does not match intended schema. {e.message}")

    restaurant_data = get_restaurant_data(restaurant_name, response_json)
    parsed_json = []
    if not restaurant_data:
        # NOTE: If JSON response is an empty array, individually
        # assign UnifiedJson object (?)
        parsed_json.append(utils.create_empty_item(restaurant_name,
                                                   area_name, lang))
    else:
        for data in restaurant_data:
            container = [get_unified_menu(option, item, day, lang)
                         for day in data.get('menus')
                         for option in day.get('mealoptions')
                         for item in option.get('menuItems')]

            restaurant_object = unified_json.RestaurantContainer(
                restaurant_name, area_name, container)
            parsed_json.append(asdict(restaurant_object))

    if parsed_json:
        parsed_json = utils.combine_restaurants(parsed_json)

    return parsed_json
