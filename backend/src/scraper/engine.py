import argparse
import itertools
import logging
import sys
from datetime import datetime, time
from pathlib import Path
from zoneinfo import ZoneInfo

from src.scraper import db_interface, utils
from src.scraper.config import CITIES
from src.scraper.parsers.compass_group.compass_group import CompassGroupParser
from src.scraper.parsers.juvenes.juvenes import JuvenesScraper
from src.scraper.parsers.sodexo.sodexo import SodexoParser

log_dir = Path("log")
log_dir.mkdir(parents=True, exist_ok=True)

logger = logging.getLogger(__name__)
logging.basicConfig(
    filename=log_dir / "webscraper_engine_run.log",
    encoding="utf-8",
    level=logging.DEBUG,
)


# def get_restaurant_url(chain: str, id: str, lang: str):
#     url = URLS.get(chain)
#     if chain == "sodexo" and lang == "en":
#         lang = "/en/"
#     if chain == "sodexo" and lang == "fi":
#         lang = "/"
#     return url.format(id=id, lang=lang)


def parse_restaurants(chain: str, area_name: str, rest_list: dict[str, str]):
    logger.info(f"Parsing {chain} in {area_name}...")
    weekly_menu = []
    chain_scrapers = {
        "juvenes": JuvenesScraper("juvenes"),
        "compass": CompassGroupParser("compass"),
        "sodexo": SodexoParser("sodexo"),
        "campusravita": JuvenesScraper("campusravita"),
        "unica": CompassGroupParser("unica"),
        # "unicafe": UnicafeParser("unicafe"),
    }
    for restaurant, id in rest_list.items():
        restaurant_menus = []
        # special case for unicafe
        # if chain == "unicafe":
        #     resp = unicafe.parse_response(restaurant, area_name, id)
        #     weekly_menu.extend(resp)
        #     continue
        print(restaurant)
        scraper = chain_scrapers.get(chain)
        if scraper is None:
            print(f"skipped chain: {chain}, {restaurant}")
        else:
            resp = scraper.handle(restaurant, area_name, id)
            restaurant_menus.extend(resp)
            weekly_menu.extend(resp)

    return weekly_menu


if __name__ == "__main__":
    # GUARDING CLAUSE FOR CRONJOB
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--peak", action="store_true", help="Specify this when running on peak hours"
    )
    args = parser.parse_args()

    now = datetime.now(ZoneInfo("Europe/Helsinki"))
    if args.peak:
        if now.weekday() > 4:
            print(f"{now}: Scraper is trying to start outside weekday. Exiting")
            sys.exit(0)
        current_time = now.time()
        start_peak_time = time(10, 30)
        end_peak_time = time(14, 0)

        if not (start_peak_time <= current_time <= end_peak_time):
            print(
                f"{now}: Scraper is trying to start outside peak hours in weekday. Exiting"
            )
            sys.exit(0)
        print(f"{now}: Scraper is running inside peak hours")
    else:
        print(f"{now}: Scraper is running outside peak hours")

    print("Running Restaurant Scraper...")
    # PARSING
    collect_data = []
    # for city_name, city_data in CITIES:
    for item in CITIES:
        city_name = item.get("name")
        default_area = item.get("default_area")
        city_data = item.get("data")

        print("===========================")
        print(f"Processing Restaurants in {city_name}...\n--------------------")
        city_data = utils.unpickled_city_dict(city_data)

        restaurants_in_city = [
            parse_restaurants(chain, area.areaName, rest_obj)
            for area in city_data
            for chain, rest_obj in area.restaurants.items()
        ]
        restaurants_in_city = list(itertools.chain.from_iterable(restaurants_in_city))

        # collect_data.append({"city": city_name, "restaurants": restaurants_in_city})
        collect_data.append(
            {
                "city": city_name,
                "default_area": default_area,
                "restaurants": restaurants_in_city,
            }
        )

        print("-----------------------")
    # Sanity check
    for item in collect_data:
        assert all(k in item.keys() for k in ["city", "restaurants"]), (
            f"Keys are not matching! item.keys() = {item.keys()}"
        )

        for rest in item["restaurants"]:
            assert all(
                k in rest.keys() for k in ["restaurant_name", "area", "menu_options"]
            ), f"Keys not matching! item.keys() = {rest.keys()}"

            logger.info(f"{rest['restaurant_name']} passed the test")

    # INSERT TO SQL
    # Create db table
    #
    db = db_interface.init_db()
    for item in collect_data:
        city = item["city"]
        default_area = item["default_area"]

        print(f"Insert restaurant menus in {city}")
        restaurant_data = item.get("restaurants")
        # city_id = db_interface.insert_city(city, db_interface.init_db())
        try:
            city_id = db_interface.insert_city(city, default_area, db)
            db_interface.insert_restaurants(city_id, restaurant_data, db)
        except Exception as e:
            db.rollback()
            logger.error(f"Failed to process city {city}. Error log: {e}")
            continue
