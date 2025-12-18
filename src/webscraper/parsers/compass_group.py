import jq
import re
import logging

from dataclasses import asdict

from webscraper.models import unified_json
from webscraper import utils

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
    food_item = food_string.split(",")
    food_item = re.split(
        r"(?:^|[^a-zA-Z])([A-Z]{1,3}|veg|Veg|VEG|vega|Vega|VEGA|\*)(?:^|[^a-zA-Z])",
        food_string,
    )
    diets = []
    for item in food_item:
        if item in DIET_CODES.keys():
            diets.append(item)
            food_item.remove(item)
    for idx, item in enumerate(diets):
        if item is "*":
            diets[idx] = "H"

    food_item = "".join(food_item)
    food = re.sub("[\*]", "", food_item).strip("()").strip()
    diets = ", ".join(diets)
    return (food, diets)


def transform_response(restaurant_name, area_name, parsed_response):
    lang = parsed_response["lang"]
    menu_options = []

    for item in parsed_response["MenusForDays"]:
        date = item.get("Date")
        date_format = "%Y-%m-%dT%H:%M:%S%z"
        date = utils.format_date(date, date_format)
        for idx, option in enumerate(item["SetMenus"]):
            menu_type = option.get("Name")
            menu_type_id = option.get("SortOrder")
            for food in option.get("Components"):
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


def parse_response(restaurant_name, area_name, lang, response_json):
    """Parse JSON response from Compass Group.
    Params:
        restaurant_name: Name of the restaurant to be queried from API.
        area_name: Area that the restaurant belongs to.
        response_json: A JSON response from Compass Group.

    Returns:
        parsed_json: A parsed JSON object hat follows the JsonTransform
        specification.
    """
    try:
        simplified_resp = (
            jq.compile("""
            del(. | .PriceHeader)
        """)
            .input_value(response_json)
            .all()
        )
    except ValueError as e:
        logger.warning(f"""{e}.
            Restaurant {restaurant_name} either has no JSON for language
            {lang} or got an unexpected JSON response
        """)
        logger.warning(
            f"Passing default formatted response for restaurant {
                restaurant_name}"
        )

        return [utils.create_empty_item(restaurant_name, area_name, lang)]

    simplified_resp = simplified_resp[0]
    simplified_resp["lang"] = lang

    formatted_response = transform_response(
        restaurant_name, area_name, simplified_resp)
    return [formatted_response]
