import os
import utils

from flask import Flask, render_template, request
from flask_apscheduler import APScheduler

from datetime import datetime

from core.config import (DEFAULT_CITY,
                         DEFAULT_DAY)

app = Flask(__name__)
scheduler = APScheduler()

scheduler.init_app(app)
scheduler.start()


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

    # Date handler
    selected_day = request.args.get('day',
                                    datetime.now().strftime("%A").lower())
    selected_date = utils.get_current_week_date(selected_day)

    # City handler
    selected_city = request.args.get('city', DEFAULT_CITY)
    cities = utils.get_cities()

    # Get all area based on selected city
    selected_area = request.args.get('area', None)
    all_areas = utils.get_all_areas(selected_city)
    if selected_area is None:
        selected_area = all_areas[0].get('area')

    # Retrieve menu based on the requested filter
    menus = utils.get_todays_menu(
        selected_city, selected_area, lang, selected_date)

    return render_template("index.html",
                           cities=cities,
                           areas=all_areas,
                           menus=menus,
                           selected_city=selected_city,
                           selected_area=selected_area,
                           day=selected_day,
                           date=selected_date,
                           lang=lang
                           )


# if __name__ == "__main__":
#
#     app.run()
