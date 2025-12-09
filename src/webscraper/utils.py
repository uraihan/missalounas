from collections import defaultdict, namedtuple
from datetime import datetime

from core.config import DATE_FORMAT


def unpickled_city_dict(city_data):
    return [namedtuple('City', data.keys())(**data)
            for data in city_data]


def combine_restaurants(weekly_menu):
    """Combine multiple restaurant entries.
    Params:
        weekly_menu: List of restaurant-food entries

    Returns:
        combined_menu: List of restaurant-food entries with duplicate
        restaurants combined together
    """
    combined_menu = defaultdict(list)
    area_set = set()
    for menu in weekly_menu:
        restaurant_name = menu['restaurant_name']
        area_set.add(menu['area'])
        options = menu['menu_options']
        # combined = {
        #     'restaurant_name': restaurant_name,
        #     'area': area,
        #     'menu_options': options
        # }
        # combined_menu.update(combined)
        combined_menu[restaurant_name].extend(options)
    if len(area_set) != 1:
        breakpoint()
    assert len(area_set) == 1, "Warning: There are more than 1 area detected"
    combined_menu = [{'restaurant_name': name,
                      "area": list(area_set)[0],
                      "menu_options": options}
                     for name, options in combined_menu.items()]

    if len(combined_menu) != 1:
        breakpoint()
    # [combined_menu] = combined_menu

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
