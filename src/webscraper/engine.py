import requests
import json
import itertools

from parsers import juvenes, compass_group, sodexo

from webscraper import utils, db_interface
from core.config import CITIES, URLS, SUPPORTED_LANGS


def get_restaurant_url(chain, id, lang):
    url = URLS.get(chain)
    if chain == "sodexo" and lang == "en":
        lang = "/en/"
    if chain == "sodexo" and lang == "fi":
        lang = "/"
    return url.format(id=id, lang=lang)


def parse_restaurants(chain, area_name, rest_list):
    print(f"Parsing {chain} in {area_name}...")
    weekly_menu = []
    for restaurant, id in rest_list.items():
        for lang in SUPPORTED_LANGS:
            try:
                # use different url based on the name of the chain
                url = get_restaurant_url(chain, id, lang=lang)
                response = requests.get(url)
                response.raise_for_status()
                response_json = json.loads(response.text)
            except requests.RequestException as e:
                print(f"Error fetching from URL: {e}")
                raise
            except ValueError as e:
                print(f"Error: {e}")
                raise

            if chain == 'juvenes':
                resp = juvenes.parse_response(
                    restaurant, area_name, lang, response_json)
            if chain == 'compass':
                resp = compass_group.parse_response(
                    restaurant, area_name, lang, response_json)
            if chain == 'sodexo':
                resp = sodexo.parse_response(
                    restaurant, area_name, lang, response_json)

            weekly_menu.extend(resp)

    # compiled_dict[chain] = chain_list
    # return compiled_dict

    return weekly_menu


if __name__ == "__main__":
    print("Running Restaurant Scraper...")
    # PARSING
    collect_data = []
    for city_name, city_data in CITIES:
        print("===========================")
        print(f"Processing {city_name}...\n--------------------")
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

            print(f"{rest["restaurant_name"]} passed the test")

    # INSERT TO SQL
    # Create db table
    db_interface.create_tables()
    for item in collect_data:
        city = item['city']
        restaurant_data = item['restaurants']
        city_id = db_interface.insert_city(city)
        db_interface.insert_restaurants(city_id, restaurant_data)
