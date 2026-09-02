from collections import defaultdict
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

import psycopg
from litestar import Request

from src.api.models import (
    MenuGroup,
    MenuItem,
    RestaurantData,
    WeeklyMenu,
)
from src.shared.config import DATE_FORMAT, DEFAULT_CITY, get_db_string


def get_cities(db: psycopg.Connection) -> list[dict[str, str | int]]:
    db_string = get_db_string()
    cities = db.execute("SELECT * FROM cities").fetchall()
    # print(cities)

    return cities


def get_all_areas(selected_city: str, db: psycopg.Connection) -> list[dict[str, str]]:
    """
    Returns: List(dict[all_areas])
    """
    db_string = get_db_string()
    areas = db.execute(
        """select distinct area from restaurants r
            left join cities c on r.city_id = c.id
            where c.name = %s
        """,
        (selected_city,),
    ).fetchall()
    # print(areas)

    return areas


def get_weekly_menu(
    city: str,
    selected_area: str,
    selected_lang: str,
    selected_date: date,
    db: psycopg.Connection,
):
    def _build_restaurant_data(
        restaurant_menus: dict[str, list[MenuGroup]],
    ) -> list[RestaurantData]:
        """Helper function to construct list of RestaurantData before returning
        get_weekly_menu function"""
        return [
            RestaurantData(restaurant_name=name, menu_group_list=groups)
            for name, groups in restaurant_menus.items()
        ]

    # current_date = datetime.now().strftime(utils.DATE_FORMAT)
    week_start = selected_date - timedelta(days=selected_date.weekday())
    week_end = week_start + timedelta(days=6)

    city_id = db.execute("SELECT id FROM cities WHERE name = %s", (city,)).fetchone()
    city_id = city_id["id"]
    query2 = """
        WITH date_series as (
            SELECT generate_series(%s::date, %s::date, '1 day'::interval) AS date
        ),
        restaurant_set AS (
            SELECT id AS restaurant_id, name AS restaurant_name
            FROM restaurants
            WHERE city_id = %s AND area = %s
        )
        SELECT
            ds.date AS date,
            rs.restaurant_name AS restaurant_name,
            f.menu_uid AS menu_uid,
            f.menu_type AS menu_type,
            ARRAY_AGG(f.name ORDER BY f.created_at) AS menu_name,
            ARRAY_AGG(f.diets) AS menu_diets
        FROM date_series ds
        CROSS JOIN restaurant_set rs
        LEFT JOIN foods f on f.restaurant_id = rs.restaurant_id
            AND f.date = ds.date
            AND f.lang = %s
        GROUP BY ds.date, rs.restaurant_name, f.menu_uid, f.menu_type
        ORDER BY ds.date, rs.restaurant_name
    """

    query = """
        SELECT
            f.date AS date,
            f.menu_uid AS menu_uid,
            r.name AS restaurant_name,
            f.menu_type AS menu_type,
            ARRAY_AGG(f.name ORDER BY f.created_at) AS menu_name,
            ARRAY_AGG(f.diets) AS menu_diets
        FROM restaurants r
        LEFT JOIN foods f ON r.id = f.restaurant_id
            AND f.date >= %s
            AND f.date <= %s
            AND f.lang = %s
        WHERE r.city_id = %s and r.area = %s
        GROUP BY r.name, f.date, f.menu_uid, f.menu_type
        ORDER BY f.date, r.name
    """

    # results = db.execute(
    #     query, (week_start, week_end, selected_lang, city_id, selected_area)
    # ).fetchall()
    results = db.execute(
        query2, (week_start, week_end, city_id, selected_area, selected_lang)
    ).fetchall()

    # todays_menu = {}
    restaurants: dict[date, dict[str, list[MenuGroup]]] = defaultdict(
        lambda: defaultdict(list)
    )
    for row in results:
        menu_date = row.get("date")
        restaurant_name = row.get("restaurant_name")
        menu_uid = row.get("menu_uid")
        menu_type = row.get("menu_type")
        foods = row.get("menu_name")
        diets = row.get("menu_diets")

        rest_list = restaurants[menu_date][restaurant_name]

        if menu_uid is None:
            # todays_menu[restaurant_name] = None
            continue

        rest_list.append(
            MenuGroup(
                uid=menu_uid,
                group_name=menu_type or "",
                menu_item_list=[
                    MenuItem(name=food, diet=diet) for food, diet in zip(foods, diets)
                ],
            )
        )

    weekly_menu = [
        WeeklyMenu(
            calendar_date=day,
            restaurant_data=_build_restaurant_data(restaurant_menus),
        )
        for day, restaurant_menus in sorted(restaurants.items())
    ]

    return weekly_menu


# NOTE: Consider changing this into solely relying on database select
# maybe by getting week number, then return monday to friday date range for that
# week?
def get_current_week_date(weekday: datetime):
    today = datetime.now(ZoneInfo("Europe/Helsinki"))
    startweek = today - timedelta(days=today.weekday())

    weekday_map = {
        "monday": 0,
        "tuesday": 1,
        "wednesday": 2,
        "thursday": 3,
        "friday": 4,
        "saturday": 5,
        "sunday": 6,
    }
    offset = weekday_map.get(weekday.lower(), 0)
    target_date = startweek + timedelta(days=offset)

    return target_date.strftime(DATE_FORMAT)


##########


# TODO: remove this in favour of using components to interact directly with
# index's query parameter
def build_url(request: Request, **queried_items):
    """
    Helper function to build a URL preserving current parameters and
    applying new ones. Only includes parameters that differ from defaults.
    """
    # Default parameters
    defaults = get_default_params(request)

    # Get current parameters
    params = {
        "day": request.query_params.get("day", defaults["day"]),
        "city": request.query_params.get("city", defaults["city"]),
        "area": request.query_params.get("area"),
        "lang": request.query_params.get("lang", defaults["lang"]),
    }

    if queried_items.get("city") and queried_items.get("city") != params.get("city"):
        params["area"] = None

    params.update(queried_items)

    returned_params = {k: v for k, v in params.items() if v != defaults.get(k)}

    return returned_params


# NOTE: This function might not be needed
def get_current_day():
    return datetime.now(ZoneInfo("Europe/Helsinki")).strftime("%A").lower()


# NOTE: THese two functions might not be needed
def get_default_params(request):
    return {
        "day": get_current_day(),
        "city": DEFAULT_CITY,
        "lang": request.accept_languages.best_match(["en", "fi"]) or "en",
    }


def get_current_params(request):
    defaults = get_default_params(request)

    return {
        "lang": request.args.get("lang", defaults["lang"]),
        "day": request.args.get("day", defaults["day"]),
        "city": request.args.get("city", defaults["city"]),
    }
