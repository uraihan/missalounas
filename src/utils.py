import psycopg

from collections import defaultdict
from datetime import datetime, timedelta

from psycopg.rows import dict_row
from core.config import db_string, DATE_FORMAT


def get_cities():
    conn = psycopg.connect(db_string, row_factory=dict_row)
    with conn:
        cities = conn.execute('SELECT * FROM cities').fetchall()

    return cities


def get_all_areas(selected_city):
    """
        Returns: List(dict[all_areas])
    """
    conn = psycopg.connect(db_string, row_factory=dict_row)
    with conn:
        areas = conn.execute('''select distinct area from restaurants r
                             left join cities c on r.city_id = c.id
                             where c.name = %s
            ''', (selected_city,)).fetchall()

    return areas


def get_todays_menu(city, selected_area, selected_lang, selected_date):
    # current_date = datetime.now().strftime(utils.DATE_FORMAT)
    conn = psycopg.connect(db_string, row_factory=dict_row)
    # all_cities = get_cities()
    with conn:
        city_id = conn.execute('SELECT id FROM cities WHERE name = %s',
                               (city,)).fetchone()
        city_id = city_id['id']
        query = '''
            SELECT
                f.menu_uid AS menu_uid,
                r.name AS restaurant_name,
                f.menu_type AS menu_type,
                ARRAY_AGG(f.name ORDER BY f.created_at) AS menu_name,
                ARRAY_AGG(f.diets) AS menu_diets
            FROM restaurants r
            LEFT JOIN foods f ON r.id = f.restaurant_id
                AND f.date = %s
                AND f.lang = %s
            WHERE r.city_id = %s and r.area = %s
            GROUP BY r.name, f.menu_uid, f.menu_type
            ORDER BY r.name
        '''

        results = conn.execute(
            query, (selected_date, selected_lang, city_id,
                    selected_area)).fetchall()

    todays_menu = {}
    for row in results:
        restaurant_name = row.get('restaurant_name')
        menu_uid = row.get('menu_uid')
        menu_type = row.get('menu_type')
        foods = row.get('menu_name')
        diets = row.get('menu_diets')

        if menu_uid is None:
            todays_menu[restaurant_name] = None
            continue

        if restaurant_name not in todays_menu:
            todays_menu[restaurant_name] = defaultdict(list)

        todays_menu[restaurant_name][menu_uid].append(
            {'menu_type': menu_type,
             'foods': [{'food_name': food, 'diet': diet}
                       for food, diet in zip(foods, diets)]
             }
        )

    return todays_menu


def get_current_week_date(weekday):
    today = datetime.now()
    startweek = today - timedelta(days=today.weekday())

    weekday_map = {
        'monday': 0,
        'tuesday': 1,
        'wednesday': 2,
        'thursday': 3,
        'friday': 4,
        'saturday': 5,
        'sunday': 6
    }
    offset = weekday_map.get(weekday.lower(), 0)
    target_date = startweek + timedelta(days=offset)

    return target_date.strftime(DATE_FORMAT)
