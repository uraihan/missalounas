from sqlalchemy import (
    Column,
    Date,
    ForeignKey,
    Integer,
    MetaData,
    Table,
    Text,
)

metadata = MetaData()

cities = Table(
    "cities",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", Text, unique=True, nullable=False),
    Column("default_area", Text, nullable=False),
)

restaurants = Table(
    "restaurants",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", Text, nullable=False),
    Column("area", Text, nullable=False),
    Column("city_id", Integer, ForeignKey("cities.id")),
)

foods = Table(
    "foods",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", Text),
    Column("diets", Text),
    Column("menu_type", Text),
    Column("menu_uid", Integer),
    Column("date", Date),
    Column("lang", Text),
    Column("restaurant_id", Integer, ForeignKey("restaurants.id")),
)
