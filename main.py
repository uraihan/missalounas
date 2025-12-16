import os
import logging

from flask import Flask, render_template, request
from flask_apscheduler import APScheduler
from datetime import datetime

from app import utils
from app.config import DEFAULT_CITY


app = Flask(__name__)
scheduler = APScheduler()

# init scheduler
scheduler.init_app(app)
scheduler.start()

# init logger
logger = logging.getLogger(__name__)
logging.basicConfig(
    filename="./log/run_scheduled_webscraper.log", encoding='utf-8')


@scheduler.task('cron',
                id='running_webscraper',
                day_of_week='mon',
                hour='00',
                minute='05')
def run_webscraper():
    logger.info(f"Starting scheduled job: Webscraping engine at {
                datetime.now()}")
    os.system('uv run src/webscraper/engine.py')


def build_url(**queried_items):
    """
    Helper function to build a URL preserving current parameters and
    applying new ones. Only includes parameters that differ from defaults.
    """
    # Default parameters
    defaults = utils.get_default_params(request)

    # Get current parameters
    params = {
        'day': request.args.get('day', defaults['day']),
        'city': request.args.get('city', defaults['city']),
        'area': request.args.get('area'),
        'lang': request.args.get('lang', defaults['lang'])
    }

    if (queried_items.get("city") and
            queried_items.get("city") != params.get("city")):
        params["area"] = None

    params.update(queried_items)

    returned_params = {k: v for k, v in params.items()
                       if v != defaults.get(k)}

    return returned_params


app.jinja_env.globals.update(build_url=build_url)


@app.context_processor
def inject_context():
    """Providing all jinja templates with global variables.
    """
    day = request.args.get('day')
    city = request.args.get('city')
    lang = request.args.get('lang')

    return {
        'selected_day': day,
        'selected_city': city,
        'lang': lang
    }


@app.get("/", endpoint="index")
def index():
    # Get current params
    current_params = utils.get_current_params(request)
    lang = current_params['lang']

    # Date handler
    selected_day = current_params['day']
    selected_date = utils.get_current_week_date(selected_day)

    # City handler
    selected_city = current_params['city']
    cities = utils.get_cities()

    # Get all area based on selected city
    selected_area = request.args.get('area', None)
    all_areas = utils.get_all_areas(selected_city)
    if selected_area is None and selected_area not in all_areas:
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
                           selected_day=selected_day,
                           date=selected_date,
                           lang=lang
                           )


if __name__ == "__main__":
    app.run()
