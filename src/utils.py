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


def get_todays_menu(city, selected_lang, selected_date):
    # current_date = datetime.now().strftime(utils.DATE_FORMAT)
    conn = psycopg.connect(db_string, row_factory=dict_row)
    # all_cities = get_cities()
    with conn:
        city_id = conn.execute('SELECT id FROM cities WHERE name = %s',
                               (city,)).fetchone()
        city_id = city_id['id']
        query = '''
            SELECT
                r.id as restaurant_id,
                r.name as restaurant_name,
                f.menu_type as menu_type,
                f.menu_type_id as menu_id,
                f.name as menu_name,
                f.diets as menu_diets
            FROM restaurants r
            LEFT JOIN foods f ON r.id = f.restaurant_id
                AND f.date = %s
                AND f.lang = %s
            WHERE r.city_id = %s
            ORDER BY r.name
        '''

        results = conn.execute(
            query, (selected_date, selected_lang, city_id)).fetchall()

    todays_menu = {}
    for row in results:
        restaurant_id = row['restaurant_id']

        if restaurant_id not in todays_menu:
            todays_menu[restaurant_id] = {
                'name': row['restaurant_name'],
                'menus': defaultdict(list)
            }
        if row['menu_name']:
            menu_id = row['menu_id']
            todays_menu[restaurant_id]['menus'][menu_id].append({
                'name': row['menu_name'],
                'diets': row['menu_diets']
            })

    for restaurant_id in todays_menu:
        todays_menu[restaurant_id]['menus'] = dict(
            todays_menu[restaurant_id]['menus'])

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
