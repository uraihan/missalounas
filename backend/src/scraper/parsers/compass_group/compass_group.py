import logging
import re
from dataclasses import asdict

import msgspec

from src.scraper import utils
from src.scraper.parsers.base import RestaurantParser
from src.scraper.parsers.compass_group.model import CompassModel
from src.shared import unified_json

logger = logging.getLogger(__name__)

DIET_CODES = {
    "*": "Healthy choice",
    "A": "Contains allergens",
    "G": "Gluten-free",
    "ILM": "Climate-friendly",
    "L": "Lactose-free",
    "M": "Dairy-free",
    "Veg": "Vegan",
    "VL": "Low lactose",
    "VS": "Contains fresh garlic",
}


def parse_dietcodes(food_string):
    # TODO: reconsider if this regex is necessary
    food_item = food_string.split(",")
    food_item = re.split(
        r"(?:^|[,\s()])([A-Z]{1,3}|veg|Veg|VEG|vega|Vega|VEGA|\*)(?:^|[,\s()])",
        food_string,
    )
    diets = []
    for item in food_item:
        if item in DIET_CODES:
            diets.append(item)
            food_item.remove(item)
    for idx, item in enumerate(diets):
        if item == "*":
            diets[idx] = "H"

    food_item = "".join(food_item)
    food = re.sub(r"[\*]", "", food_item).strip("()").strip()
    diets = ", ".join(diets)
    return (food, diets)


class CompassGroupParser(RestaurantParser):
    def _transform_response(
        self,
        restaurant_name: str,
        area_name: str,
        parsed_response: CompassModel,
        lang: str,
    ):
        # lang = parsed_response["lang"]
        menu_options = []

        if not parsed_response.menus_for_days:
            menu_options.append(
                utils.create_empty_item(restaurant_name, area_name, lang)
            )
        else:
            for item in parsed_response.menus_for_days:
                date = item.date
                date_format = "%Y-%m-%dT%H:%M:%S%z"
                date = utils.format_date(date, date_format)

                for idx, option in enumerate(item.set_menus):
                    menu_type = option.name
                    menu_type_id = option.sort_order
                    for food in option.components:
                        food_name, diets = parse_dietcodes(food)
                        menu_item = unified_json.IndividualMenu(
                            food_name,
                            diets,
                            menu_type=menu_type,
                            date=date,
                            menu_uid=menu_type_id,
                            lang=lang,
                        )
                        menu_options.append(menu_item)

        restaurant_dict = unified_json.RestaurantContainer(
            restaurant_name, area_name, menu_options
        )
        return asdict(restaurant_dict)

    def build_url(self, restaurant_id: str, lang: str) -> str:
        return self.url_template.format(id=restaurant_id, lang=lang)

    def parse_response(
        self, restaurant_name: str, area_name: str, lang: str, response_json
    ):
        """Parse JSON response from Compass Group.
        Params:
            restaurant_name: Name of the restaurant to be queried from API.
            area_name: Area that the restaurant belongs to.
            response_json: A JSON response from Compass Group.

        Returns:
            parsed_json: A parsed JSON object hat follows the JsonTransform
            specification.
        """
        simplified_resp = msgspec.convert(response_json, type=CompassModel)

        formatted_response = self._transform_response(
            restaurant_name, area_name, simplified_resp, lang
        )
        return [formatted_response]
