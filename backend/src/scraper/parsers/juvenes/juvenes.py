import logging
from dataclasses import asdict
from itertools import chain
from typing import override

import msgspec

from src.scraper import utils
from src.scraper.parsers.base import RestaurantParser
from src.shared import unified_json

from .model import (
    Day,
    JuvenesModel,
    MealOption,
    Menu,
    MenuItem,
    MenuType,
    SimplifiedDay,
    SimplifiedMealOption,
    SimplifiedMenuItem,
    SimplifiedMenuType,
)
from .restaurant_id_lookup import RESTAURANT_UNIQUE_IDS

logger = logging.getLogger(__name__)


def get_essential_chunk(
    response: list[JuvenesModel], sub_rest_id: list[int]
) -> list[MenuType]:
    response_object = response[0]
    result: list[MenuType] = []
    for id in sub_rest_id:
        for menu_type in response_object.menu_types:
            if menu_type.menu_type_id == id:
                result.append(menu_type)

    return result


def flatten_menu_item(item: MenuItem) -> SimplifiedMenuItem:
    return SimplifiedMenuItem(
        name=item.name, diets=item.diets, ingredients=item.ingredients
    )


def flatten_mealoption(mealoption: MealOption) -> SimplifiedMealOption:
    return SimplifiedMealOption(
        name=mealoption.name,
        order_number=mealoption.order_number,
        menu_items=list(map(flatten_menu_item, mealoption.menu_items)),
    )


def flatten_day(day: Day) -> SimplifiedDay:
    response_format = "%Y%m%d"
    return SimplifiedDay(
        date=utils.format_date(str(day.date), response_format),
        mealoptions=list(map(flatten_mealoption, day.mealoptions)),
    )


def simplify_day(menu: Menu) -> list[SimplifiedDay]:
    return [flatten_day(day) for day in menu.days]


def simplify_menu_types(essential_chunk: list[MenuType]) -> list[SimplifiedMenuType]:
    """
    For each MenuType, flattens every day inside every menu into a flat list of {date, mealoptions} entries, keeping only the fields downstream code actually needs.
    """
    return [
        SimplifiedMenuType(
            menu_type_name=item.menu_type_name,
            restaurant_unique_id=item.menu_type_id,
            menus=list(chain.from_iterable(simplify_day(menu) for menu in item.menus)),
        )
        for item in essential_chunk
    ]


def get_unified_menu(menu_option, menu_item, day, lang):
    """Form a unified menu container."""
    food_list = unified_json.IndividualMenu(
        food_name=menu_item.name,
        diets=menu_item.diets,
        menu_type=menu_option.name,
        date=day.date,
        menu_uid=menu_option.order_number,
        lang=lang,
    )

    return food_list


class JuvenesScraper(RestaurantParser):
    def _get_restaurant_data(
        self, restaurant_name: str, response_json: list[JuvenesModel]
    ) -> list[SimplifiedMenuType]:
        """Get the relevant restaurant data from JSON response.
        Params:
            restaurant_name: Name of restaurant associated with the provided
                response_json.
            response_json: JSON response from the API

        Returns:
            restaurant_data: Trimmed down version of the JSON response.
        """
        sub_restaurant_id = RESTAURANT_UNIQUE_IDS.get(restaurant_name)
        essential_chunk = get_essential_chunk(response_json, sub_restaurant_id)
        simplified_resp = simplify_menu_types(essential_chunk)

        # restaurant_data = []
        # for item in simplified_resp:
        #     for menu in item.menus:
        #         response_format = "%Y%m%d"
        #         menu.date = utils.format_date(str(menu.date), response_format)
        #     restaurant_data.append(item)

        # return restaurant_data
        return simplified_resp

    def build_url(self, restaurant_id: str, lang: str) -> str:
        return self.url_template.format(id=restaurant_id, lang=lang)

    @override
    def parse_response(
        self, restaurant_name: str, area_name: str, lang: str, response_json
    ) -> list[dict]:
        """Parse JSON response from Juvenes.
        Params:
            restaurant_name: Name of the restaurant to be queried from API.
            area_name: Area that the restaurant belongs to.
            response_json: A JSON response from Juvenes.

        Returns:
            parsed_json: A parsed JSON object hat follows the JsonTransform
            specification.
        """

        # for debugging purpose, use a test json file
        if not response_json:
            return [utils.create_empty_item(restaurant_name, area_name, lang)]
        else:
            parsed_response = msgspec.convert(response_json, type=list[JuvenesModel])
            restaurant_data = self._get_restaurant_data(
                restaurant_name, parsed_response
            )

            parsed_json = []
            for data in restaurant_data:
                container = [
                    get_unified_menu(option, item, day, lang)
                    for day in data.menus
                    for option in day.mealoptions
                    for item in option.menu_items
                ]

                restaurant_object = unified_json.RestaurantContainer(
                    restaurant_name, area_name, container
                )
                parsed_json.append(asdict(restaurant_object))

        # if parsed_json:
        #     parsed_json = utils.combine_restaurants(parsed_json)

        return parsed_json
