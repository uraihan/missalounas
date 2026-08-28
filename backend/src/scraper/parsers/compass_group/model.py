import msgspec


class SetMenu(msgspec.Struct, rename="pascal"):
    sort_order: int
    components: list[str]
    name: str | None = None
    price: str | None = None


class MenuForDay(msgspec.Struct, rename="pascal"):
    date: str
    lunch_time: str | None
    set_menus: list[SetMenu]


class CompassModel(msgspec.Struct, rename="pascal"):
    error_text: str | None  # TODO: if error text return something do something
    restaurant_name: str | None = None
    restaurant_url: str | None = None
    price_header: str | None = None
    menus_for_days: list[MenuForDay] | None = None
    footer: str | None = None
