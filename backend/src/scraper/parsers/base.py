import logging
import time
from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor

import requests
from requests.adapters import HTTPAdapter, Retry

from src.scraper.config import SUPPORTED_LANGS, URLS
from src.scraper.utils import combine_restaurants

logger = logging.getLogger(__name__)

session = requests.Session()
session.mount(
    "https://",
    HTTPAdapter(
        max_retries=Retry(total=5, backoff_factor=5, status_forcelist=[502, 503, 504])
    ),
)


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
        start_time = time.time()
        response = session.get(url)
        response.raise_for_status()
        total_time = time.time() - start_time
        print(f"Completed fetching menu in {total_time} seconds")
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

        def fetch_and_parse(lang: str) -> list[dict]:
            url = self.build_url(restaurant_id, lang)
            response_json = fetch_json(url)
            return self.parse_response(restaurant_name, area_name, lang, response_json)

        with ThreadPoolExecutor(max_workers=len(SUPPORTED_LANGS)) as pool:
            results = pool.map(fetch_and_parse, SUPPORTED_LANGS)
            # menus.extend(
            #     self.parse_response(restaurant_name, area_name, lang, response_json)
            # )

        menus = [item for sublist in results for item in sublist]
        return combine_restaurants(menus)
