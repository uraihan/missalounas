import logging
from abc import ABC, abstractmethod

import requests

from src.scraper.config import SUPPORTED_LANGS, URLS
from src.scraper.utils import combine_restaurants

logger = logging.getLogger(__name__)


class GenericRestaurantParser[RestaurantId: str | list[str]](ABC):
    def __init__(self, chain: str) -> None:
        self.url_template = URLS.get(chain)

    @abstractmethod
    def handle(
        self,
        restaurant_name: str,
        area_name: str,
        restaurant_id: RestaurantId,
    ) -> list[dict]: ...


def fetch_json(url: str):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Error fetching data from {url}: {e}")
        raise
    except ValueError as e:
        logger.error(f"Error decoding JSON response from {url}: {e}")
        raise


class RestaurantParser(GenericRestaurantParser, ABC):
    @abstractmethod
    def build_url(self, restaurant_id: str, lang: str) -> str: ...

    @abstractmethod
    def parse_response(
        self, restaurant_name: str, area_name: str, lang: str, response_json
    ) -> list[dict]: ...

    def handle(
        self,
        restaurant_name: str,
        area_name: str,
        restaurant_id: str,
    ) -> list[dict]:
        menus = []
        for lang in SUPPORTED_LANGS:
            url = self.build_url(restaurant_id, lang)
            response_json = fetch_json(url)
            menus.extend(
                self.parse_response(restaurant_name, area_name, lang, response_json)
            )

        return combine_restaurants(menus)
