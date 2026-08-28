from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from datetime import date, datetime
from zoneinfo import ZoneInfo

import psycopg
from litestar import Litestar, get
from litestar.di import NamedDependency, Provide
from litestar.openapi import OpenAPIConfig
from litestar.params import FromQuery

from src.api import utils
from src.api.db import create_pool, provide_db
from src.api.models import WeeklyMenu


@asynccontextmanager
async def lifespan(app: Litestar) -> AsyncIterator[None]:
    app.state.pool = create_pool()
    app.state.pool.open()
    try:
        yield
    finally:
        app.state.pool.close()


# ROUTES
# TODO: Think of better way to structure this
@get("/menu")
async def get_menu(
    db: NamedDependency[psycopg.Connection],
    day: FromQuery[date | None] = None,
    city: FromQuery[str | None] = "Tampere",
    area: FromQuery[str | None] = "Hervanta",
    lang: FromQuery[str | None] = "fi",
) -> list[WeeklyMenu]:
    if day is None:
        day = datetime.now(tz=ZoneInfo("Europe/Helsinki")).date()

    selected_date = day
    # selected_date = utils.get_current_week_date(day)
    # all_cities = utils.get_cities(db)
    # all_areas = utils.get_all_areas(city, db)

    menus = utils.get_weekly_menu(city, area, lang, selected_date, db)
    print(menus)

    return menus


@get("/cities")
async def get_cities(
    db: NamedDependency[psycopg.Connection],
) -> list[dict[str, str | int]]:
    return utils.get_cities(db)


@get("/areas")
async def get_areas(
    db: NamedDependency[psycopg.Connection], city: FromQuery[str]
) -> list[dict[str, str]]:
    return utils.get_all_areas(city, db)


route_handlers = [get_menu, get_cities, get_areas]

app = Litestar(
    route_handlers=route_handlers,
    lifespan=[lifespan],
    dependencies={"db": Provide(provide_db)},
    openapi_config=OpenAPIConfig(title="Missalounas API", version="0.5"),
)
