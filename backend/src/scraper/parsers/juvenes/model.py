import datetime

from msgspec import Struct


class MenuItem(Struct, rename="camel"):
    name: str
    order_number: int
    portion_size: int
    diets: str
    ingredients: str
    # images: list[str] = []


class MealOption(Struct, rename="camel"):
    name: str
    order_number: int
    id: int
    menu_items: list[MenuItem]


class Day(Struct, rename="camel"):
    date: int
    weekday: int
    mealoptions: list[MealOption]
    lang: str


class Menu(Struct, rename="camel"):
    menu_name: str
    menu_additional_name: str
    menu_id: int
    days: list[Day]


class MenuType(Struct, rename="camel"):
    menu_type_id: int
    menu_type_name: str
    menus: list[Menu]


class JuvenesModel(Struct, rename="camel"):
    kitchen_name: str
    kitchen_id: int
    address: str
    city: str
    email: str
    phone: str
    info: str
    menu_types: list[MenuType]


## Simplified/flattened Model ##
class SimplifiedMenuItem(Struct, rename="camel"):
    name: str
    diets: str
    ingredients: str


class SimplifiedMealOption(Struct, rename="camel"):
    name: str
    order_number: int
    menu_items: list[SimplifiedMenuItem]


class SimplifiedDay(Struct, rename="camel"):
    date: datetime.date
    mealoptions: list[SimplifiedMealOption]


class SimplifiedMenuType(Struct, rename="camel"):
    menu_type_name: str
    restaurant_unique_id: int
    menus: list[SimplifiedDay]
