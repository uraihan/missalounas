import requests
import json
import itertools
import logging

from parsers import juvenes, compass_group, sodexo, unicafe

from webscraper import utils, db_interface
from webscraper.config import CITIES, URLS, SUPPORTED_LANGS

logger = logging.getLogger(__name__)
logging.basicConfig(filename='./log/webscraper_engine_run.log',
                    encoding='utf-8',
                    level=logging.DEBUG)


def get_restaurant_url(chain, id, lang):
    url = URLS.get(chain)
    if chain == "sodexo" and lang == "en":
        lang = "/en/"
    if chain == "sodexo" and lang == "fi":
        lang = "/"
    return url.format(id=id, lang=lang)


def parse_restaurants(chain, area_name, rest_list):
    logger.info(f"Parsing {chain} in {area_name}...")
    weekly_menu = []
    for restaurant, id in rest_list.items():
        restaurant_menus = []
        # special case for unicafe
        if chain == "unicafe":
            resp = unicafe.parse_response(restaurant, area_name, id)
            weekly_menu.extend(resp)
            continue

        for lang in SUPPORTED_LANGS:
            try:
                # use different url based on the name of the chain
                url = get_restaurant_url(chain, id, lang=lang)
                response = requests.get(url)
                response.raise_for_status()
                response_json = response.json()
            except requests.RequestException as e:
                logger.error(f"Error fetching from URL: {e}")
                print("An error was encountered. Check the logfile.")
                raise
            except ValueError as e:
                logger.error(f"Error: {e}")
                print("An error was encountered. Check the logfile.")
                raise

            if chain == "juvenes":
                resp = juvenes.parse_response(
                    restaurant, area_name, lang, response_json
                )
            if chain == "compass" or chain == "unica":
                resp = compass_group.parse_response(
                    restaurant, area_name, lang, response_json
                )
            if chain == "sodexo":
                resp = sodexo.parse_response(restaurant, area_name, lang, response_json)
            if chain == "campusravita":
                resp = juvenes.parse_response(
                    restaurant, area_name, lang, response_json
                )

            restaurant_menus.extend(resp)

        # combine english and finnish menus
        weekly_menu.extend(utils.combine_restaurants(restaurant_menus))

    return weekly_menu


if __name__ == "__main__":
    print("Running Restaurant Scraper...")
    # PARSING
    collect_data = []
    for city_name, city_data in CITIES:
        print("===========================")
        print(f"Processing Restaurants in {city_name}...\n--------------------")
        city_data = utils.unpickled_city_dict(city_data)

        restaurants_in_city = [
            parse_restaurants(chain, area.areaName, rest_obj)
            for area in city_data
            for chain, rest_obj in area.restaurants.items()
        ]
        restaurants_in_city = list(itertools.chain.from_iterable(
            restaurants_in_city))

        collect_data.append(
            {'city': city_name,
             'restaurants': restaurants_in_city}
        )

        print("-----------------------")
    # Sanity check
    for item in collect_data:
        assert (all(k in item.keys() for k in ['city',
                                               'restaurants'])), (
            f"Keys are not matching! item.keys() = {item.keys()}")

        for rest in item['restaurants']:
            assert (all(k in rest.keys() for k in ['restaurant_name',
                                                   'area',
                                                   'menu_options'])), (
                f"Keys not matching! item.keys() = {rest.keys()}")

            logger.info(f"{rest["restaurant_name"]} passed the test")

    # INSERT TO SQL
    # Create db table
    print("Creating tables...")
    db_interface.create_tables()
    for item in collect_data:
        city = item['city']
        print(f"Insert restaurant menus in {city}")
        restaurant_data = item.get('restaurants')
        city_id = db_interface.insert_city(city)
        db_interface.insert_restaurants(city_id, restaurant_data)
