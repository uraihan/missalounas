import requests
import json
import sqlite3
import os

from parsers import juvenes, compass_group, sodexo

from webscraper import utils
from core.config import CITIES, URLS, SUPPORTED_LANGS
from webscraper.db import db_interface


def get_restaurant_url(chain, id, lang):
    url = URLS.get(chain)
    if chain == "sodexo" and lang == "en":
        lang = "/en/"
    if chain == "sodexo" and lang == "fi":
        lang = "/"
    return url.format(id=id, lang=lang)


def parse_restaurants(chain, rest_list):
    print(f"Parsing {chain}...")
    weekly_menu = []
    for id, loc in rest_list.items():
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
                resp = juvenes.parse_response(id, lang, response_json)
            if chain == 'compass':
                resp = compass_group.parse_response(id, lang, response_json)
            if chain == 'sodexo':
                resp = sodexo.parse_response(id, lang, response_json)

            weekly_menu.extend(resp)

    # compiled_dict[chain] = chain_list
    # return compiled_dict
    combined_menu = utils.combine_restaurants(weekly_menu)

    return combined_menu


if __name__ == "__main__":
    print("Running Restaurant Scraper...")
    # PARSING
    city_data = []
    for city, rest_dict in CITIES:
        restaurant_menus = []
        for chain, rest_list in rest_dict.items():
            weekly_menu = parse_restaurants(chain, rest_list)
            restaurant_menus.extend(weekly_menu)
        city_data.append({'city': city, 'restaurant_menus': restaurant_menus})

    # INSERT TO SQL
    # Create db table
    # breakpoint()
    db_interface.create_tables()
    for item in city_data:
        city = item['city']
        weekly_menu = item['restaurant_menus']
        city_id = db_interface.insert_city(city)
        db_interface.insert_restaurants(city_id, weekly_menu)
