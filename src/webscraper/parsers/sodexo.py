import jq
import logging

from datetime import datetime, timedelta
from dataclasses import asdict

from webscraper import utils
from webscraper.models import unified_json

logger = logging.getLogger(__name__)


def get_restaurant_data(response_json):
    restaurant_data = {}
    if not response_json:
        return response_json
    weekly_menu = response_json['mealdates']
    weekly_menu = jq.compile('''
        .[] | del(.courses[] | .meal_category, .price,
                  (.additionalDietInfo.dietcodeImages))
    ''').input_value(weekly_menu).all()

    # TODO:
    restaurant_data['restaurant_name'] = response_json['meta']['ref_title']
    generated_timestamp = response_json['meta']['generated_timestamp']
    restaurant_data['datetime'] = datetime.fromtimestamp(
        generated_timestamp)
    restaurant_data['timeperiod'] = response_json['timeperiod']
    restaurant_data['weekly_menus'] = [menu for menu in weekly_menu]

    return restaurant_data


def parse_response(restaurant_name, area_name, lang, response_json):
    """Parse JSON response from Sodexo.
    Params:
        restaurant_name: Restaurant name to be queried from API.
        area_name: Area that the restaurant belongs to.
        response_json: A JSON response from Sodexo.

    Returns:
        parsed_json: A parsed JSON object hat follows the JsonTransform
        specification.
    """
    restaurant_data = get_restaurant_data(response_json)
    if not restaurant_data:
        food_item = unified_json.IndividualMenu(food_name=None,
                                                diets=None,
                                                date=None,
                                                menu_type=None,
                                                menu_type_id=None,
                                                lang=lang)
        parsed_json = unified_json.UnifiedJson(
            restaurant_name, area_name, [food_item])

    else:
        restaurant_name = restaurant_data['restaurant_name']
        parsed_time = restaurant_data['datetime']
        # time_period = restaurant_data['timeperiod']
        year, week, _ = parsed_time.isocalendar()

        menu_list = []
        for num, day in enumerate(restaurant_data['weekly_menus']):
            date = datetime.fromisocalendar(
                year, week, num+1).strftime(utils.DATE_FORMAT)
            for _, option in day['courses'].items():
                food_name = option[f'title_{lang}']
                menu_type = option['category']
                if 'meal_category' in option.keys():
                    menu_type_id = option['meal_category']
                else:
                    menu_type_id = 0

                if 'dietcodes' in option.keys():
                    diets = option['dietcodes']
                else:
                    diets = ""

                food_item = unified_json.IndividualMenu(food_name,
                                                        diets,
                                                        date,
                                                        menu_type,
                                                        menu_type_id,
                                                        lang)
                menu_list.append(food_item)

        parsed_json = unified_json.UnifiedJson(
            restaurant_name, area_name, menu_list)

    return [asdict(parsed_json)]
