from collections import defaultdict
from datetime import datetime

from app.core.config import DATE_FORMAT


def combine_restaurants(weekly_menu):
    """Combine multiple restaurant entries.
    Params:
        weekly_menu: List of restaurant-food entries

    Returns:
        combined_menu: List of restaurant-food entries with duplicate
        restaurants combined together
    """
    combined_menu = defaultdict(list)
    for menu in weekly_menu:
        restaurant_name = menu['restaurant_name']
        options = menu['menu_options']
        combined_menu[restaurant_name].extend(options)
    combined_menu = [{'restaurant_name': name, "menu_options": options}
                     for name, options in combined_menu.items()]

    return combined_menu


def format_date(original_date, response_format):
    date_format = DATE_FORMAT
    try:
        datetime_fmt = datetime.strptime(
            str(original_date), response_format)
        datetime_fmt = f"{datetime_fmt.strftime(date_format)}"
    except Exception as e:
        raise f"Error converting date: {e}"

    return datetime_fmt
