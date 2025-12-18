from collections import defaultdict, namedtuple
from datetime import datetime
from dataclasses import asdict

from app.config import DATE_FORMAT
from webscraper.models import unified_json


def unpickled_city_dict(city_data):
    return [namedtuple('City', data.keys())(**data)
            for data in city_data]


def combine_restaurants(weekly_menu):
    """Combine multiple restaurant entries.
    Params:
        weekly_menu: List of restaurant-food entries

    Returns:
        combined_menu: List of restaurant-food entries with duplicate
        restaurants combined together
    """
    area_set = {menu.get('area') for menu in weekly_menu}

    combined_menu = defaultdict(list)
    for menu in weekly_menu:
        restaurant_name = menu.get('restaurant_name')
        options = menu.get('menu_options')
        combined_menu[restaurant_name].extend(options)

    return [{'restaurant_name': name,
             "area": list(area_set)[0],
             "menu_options": option}
            for name, option in combined_menu.items()]


def format_date(original_date, response_format, year=None):
    date_format = DATE_FORMAT
    try:
        datetime_fmt = datetime.strptime(
            str(original_date), response_format)
        if year:
            datetime_fmt = datetime_fmt.replace(year)
        datetime_fmt = f"{datetime_fmt.strftime(date_format)}"
    except Exception as e:
        raise  # f"Error converting date: {e}"

    return datetime_fmt


def create_empty_item(restaurant_name, area_name, lang):
    """Create an empty Restaurant item if parser cannot find the menu.
    Returns:
        restaurant (dict(Unified_Json))
    """

    no_food = unified_json.IndividualMenu(food_name=None,
                                          diets=None,
                                          menu_type=None,
                                          date=None,
                                          menu_uid=None,
                                          lang=lang)

    return asdict(unified_json.RestaurantContainer(restaurant_name=restaurant_name,
                                                   area=area_name,
                                                   menu_options=[no_food]
                                                   ))
