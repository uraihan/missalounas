import logging
from dataclasses import asdict
from datetime import datetime

import msgspec

from src.scraper import utils
from src.scraper.parsers.base import RestaurantParser
from src.scraper.parsers.sodexo.model import SodexoModel
from src.shared import unified_json

logger = logging.getLogger(__name__)


class SodexoParser(RestaurantParser):
    # def _get_restaurant_data(self, response_json):
    #     # replace with msgspec
    #     restaurant_data = {}
    #     if not response_json:
    #         return response_json
    #     weekly_menu = response_json["mealdates"]
    #     weekly_menu = (
    #         jq.compile("""
    #         .[] | del(.courses[] | .meal_category, .price,
    #                   (.additionalDietInfo.dietcodeImages))
    #     """)
    #         .input_value(weekly_menu)
    #         .all()
    #     )
    #
    #     # TODO:
    #     restaurant_data["restaurant_name"] = response_json["meta"]["ref_title"]
    #     generated_timestamp = response_json["meta"]["generated_timestamp"]
    #     restaurant_data["datetime"] = datetime.fromtimestamp(generated_timestamp)
    #     restaurant_data["timeperiod"] = response_json["timeperiod"]
    #     restaurant_data["weekly_menus"] = [menu for menu in weekly_menu]
    #
    #     return restaurant_data

    def build_url(self, restaurant_id: str, lang: str) -> str:
        if lang == "en":
            lang = "/en/"
        if lang == "fi":
            lang = "/"
        return self.url_template.format(id=restaurant_id, lang=lang)

    def parse_response(
        self, restaurant_name: str, area_name: str, lang: str, response_json
    ):
        """Parse JSON response from Sodexo.
        Params:
            restaurant_name: Restaurant name to be queried from API.
            area_name: Area that the restaurant belongs to.
            response_json: A JSON response from Sodexo.

        Returns:
            parsed_json: A parsed JSON object hat follows the JsonTransform
            specification.
        """
        # restaurant_data = _get_restaurant_data(response_json)
        if not response_json:
            return [utils.create_empty_item(restaurant_name, area_name, lang)]

        try:
            restaurant_data = msgspec.convert(response_json, type=SodexoModel)
        except Exception:
            print(
                f"Error converting data to msgspec model. JSON Data:\n{response_json}"
            )
            raise

        restaurant_name = restaurant_data.meta.ref_title
        parsed_time = datetime.fromtimestamp(restaurant_data.meta.generated_timestamp)
        year, week, _ = parsed_time.isocalendar()

        menu_list = []
        for num, day in enumerate(restaurant_data.mealdates):
            date = datetime.fromisocalendar(year, week, num + 1).date()  # .strftime(
            # print(date)
            # breakpoint()
            # utils.DATE_FORMAT
            # )
            for option in day.courses.values():
                food_name = option.title_en if lang == "en" else option.title_fi
                menu_type = option.category
                menu_type_id = (
                    int(option.meal_category)
                    if option.meal_category and option.meal_category.isdigit()
                    else 0
                )
                diets = option.dietcodes if option.dietcodes else ""

                food_item = unified_json.IndividualMenu(
                    food_name,
                    diets,
                    menu_type=menu_type,
                    date=date,
                    menu_uid=menu_type_id,
                    lang=lang,
                )
                menu_list.append(food_item)

        parsed_json = asdict(
            unified_json.RestaurantContainer(restaurant_name, area_name, menu_list)
        )

        return [parsed_json]
