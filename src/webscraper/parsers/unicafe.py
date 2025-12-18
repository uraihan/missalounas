# NOTE: Almost prod ready
import requests
import locale

from webscraper import utils, config
from datetime import datetime
from dataclasses import asdict

import logging
from webscraper.models import unified_json

logger = logging.getLogger(__name__)


class _DotDict(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


def get_essential_chunk(response, rest_id):
    for item in response:
        if item.get('id') == int(rest_id):
            return item


def parse_response(restaurant_name, area_name, ids):
    """Parse JSON response from Unicafe. Due to specific nature of Unicafe's
    API response, all restaurants and menu language will be handled directly
    within this module.
    Params:
        restaurant_name: Name of the restaurant to be queried from API.
        area_name: Area that the restaurant belongs to.
        ids: List of restaurant IDs, with format ['en_id', 'fi_id'].

    Returns:
        parsed_json: A parsed JSON object hat follows the JsonTransform
        specification.
    """
    current_year = datetime.now().year
    date_format = "%a %d.%m."
    original_locale = locale.setlocale(locale.LC_ALL)
    parsed_json = []
    for idx, lang in enumerate(config.SUPPORTED_LANGS):  # ['en', 'fi']
        if lang == 'fi':
            locale.setlocale(locale.LC_ALL, 'fi_FI.UTF-8')
        url = config.URLS.get("unicafe").format(lang=lang)
        try:
            response = requests.get(url)
            response.raise_for_status()
            response_json = response.json(object_hook=_DotDict)
        except requests.RequestException as e:
            logger.error(f"Error fetching from URL: {e}")
            print("An error was encountered. Check the logfile.")
            raise
        except ValueError as e:
            logger.error(f"Error: {e}")
            print("An error was encountered. Check the logfile.")
            raise

        response_json = get_essential_chunk(response_json, ids[idx])

        for data in response_json.menuData.menus:
            date = utils.format_date(data.date,
                                     date_format,
                                     year=current_year)
            day_menu = []
            for item in data.data:
                food_name = item.name
                food_diet = item.meta.get('0')
                food_diet = [diet for diet in food_diet if diet != "KELA"]
                food_diet = ", ".join(food_diet)
                menu_type = item.price.name
                menu_uid = 0  # change this. unicafe does not have menuid
                menu_item = unified_json.IndividualMenu(food_name,
                                                        food_diet,
                                                        menu_type,
                                                        date,
                                                        menu_uid,
                                                        lang)
                day_menu.append(menu_item)

            restaurant_container = unified_json.RestaurantContainer(
                restaurant_name, area_name, day_menu)
            parsed_json.append(asdict(restaurant_container))

    locale.setlocale(locale.LC_ALL, original_locale)
    return parsed_json
