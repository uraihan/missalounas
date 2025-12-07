import sqlite3
from flask import Flask, render_template, request
import psycopg

from datetime import datetime, timedelta
from collections import defaultdict
from urllib.parse import urlencode

# from app.services import utils
from core.config import DEFAULT_CITY, DEFAULT_DAY, DATE_FORMAT, db_name, db_type, db_user

app = Flask(__name__)

db_string = f"dbname={db_name} user={db_user}"


# def db_connection():
#     conn = sqlite3.connect('mock_db.db')
#     conn.row_factory = sqlite3.Row
#     return conn


def get_cities():
    conn = psycopg.connect(db_string)
    with conn:
        cities = conn.execute('SELECT * FROM cities').fetchall()

    return cities


def get_todays_menu(city, selected_lang, selected_date):
    # current_date = datetime.now().strftime(utils.DATE_FORMAT)
    conn = psycopg.connect(db_string)
    # all_cities = get_cities()
    with conn:
        city_id = conn.execute('SELECT id FROM cities WHERE name = ?',
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
                AND f.date = ?
                AND f.lang = ?
            WHERE r.city_id = ?
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


def build_url(**new_params):
    """
    Build a URL preserving current parameters and applying new ones.
    Only includes parameters that differ from defaults.
    """
    # Get current parameters
    current_params = {
        'day': request.args.get('day', DEFAULT_DAY),
        'city': request.args.get('city', DEFAULT_CITY),
        'lang': request.args.get('lang',
                                 request.accept_languages.best_match(['fi', 'en']) or 'en')
    }

    # Update with new parameters
    current_params.update(new_params)

    # Filter out default values
    filtered_params = {}
    defaults = {
        'day': DEFAULT_DAY,
        'city': DEFAULT_CITY,
        'lang': request.accept_languages.best_match(['fi', 'en']) or 'en'
    }

    for key, value in current_params.items():
        if value != defaults.get(key):
            filtered_params[key] = value

    return filtered_params


app.jinja_env.globals.update(build_url=build_url)


@app.context_processor
def inject_context():
    day = request.args.get('day')
    city = request.args.get('city')
    lang = request.args.get('lang')

    return {
        'current_day': day,
        'current_city': city,
        'current_lang': lang
    }


@app.get("/", endpoint="index")
def index(day=None, city=None, lang=None):
    # Get default arguments
    lang = request.args.get('lang')
    if lang is None:
        lang = request.accept_languages.best_match(['fi', 'en']) or 'en'

    selected_day = request.args.get('day',
                                    datetime.now().strftime("%A").lower())
    selected_city = request.args.get('city', DEFAULT_CITY)

    # Date handling
    selected_date = get_current_week_date(selected_day)

    # selected_date = '28.11.2025'
    # Handling city
    cities = get_cities()

    # Retrieve menu based on requested filter
    menus = get_todays_menu(selected_city, lang, selected_date)

    return render_template("index.html",
                           cities=cities,
                           menus=menus,
                           selected_city=selected_city,
                           lang=lang,
                           day=selected_day,
                           date=selected_date
                           )
