from datetime import date

import msgspec


class MenuItem(msgspec.Struct):
    name: str
    diet: str  # consider list[str], which then we can make STRenum for diet code


class MenuGroup(msgspec.Struct):
    uid: int
    group_name: str
    menu_item_list: list[MenuItem]


class RestaurantData(msgspec.Struct):
    restaurant_name: str
    menu_group_list: list[MenuGroup]


class WeeklyMenu(msgspec.Struct):
    calendar_date: date
    restaurant_data: list[RestaurantData]
