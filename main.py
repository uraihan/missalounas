import psycopg
import os
import utils

from psycopg.rows import dict_row
from flask import Flask, render_template, request
from flask_apscheduler import APScheduler

from datetime import datetime

from core.config import (DEFAULT_CITY,
                         DEFAULT_DAY,
                         db_string)

app = Flask(__name__)
scheduler = APScheduler()

scheduler.init_app(app)
scheduler.start()


# def db_connection():
#     conn = sqlite3.connect('mock_db.db')
#     conn.row_factory = sqlite3.Row
#     return conn


@scheduler.task('cron',
                id='running_webscraper',
                day_of_week='mon',
                hour='00',
                minute='05')
def run_webscraper():
    os.system('uv run src/webscraper/engine.py')


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
    selected_date = utils.get_current_week_date(selected_day)

    # selected_date = '28.11.2025'
    # Handling city
    cities = utils.get_cities()

    # Retrieve menu based on requested filter
    menus = utils.get_todays_menu(selected_city, lang, selected_date)

    return render_template("index.html",
                           cities=cities,
                           menus=menus,
                           selected_city=selected_city,
                           lang=lang,
                           day=selected_day,
                           date=selected_date
                           )


# if __name__ == "__main__":
#
#     app.run()
