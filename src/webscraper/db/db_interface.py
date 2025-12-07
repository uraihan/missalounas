import sqlite3
import os
import psycopg

# from psycopg_pool import ConnectionPool
# from datetime import datetime
# from sqlalchemy.orm import declarative_base, sessionmaker

from core.config import db_type, db_name, db_user
# from app.models.db_schema import Cities, Restaurants, Foods

# db_path = os.path.abspath('mock_db2.db')
# conn = sqlite3.connect(db_path)


db_string = f"dbname={db_name} user={db_user}"


def create_tables():
    conn_pg = psycopg.connect(db_string)
    with conn_pg as conn:

        cursor = conn.cursor()
        # comment off if using sqlite
        # cursor.execute("PRAGMA foreign_keys = ON")

        # Very dirty solution > need to come up with better one
        cursor.execute("DROP TABLE IF EXISTS foods")
        cursor.execute("DROP TABLE IF EXISTS restaurants")
        cursor.execute("DROP TABLE IF EXISTS cities")

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cities (
                id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
                name VARCHAR(200) NOT NULL UNIQUE
                )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS restaurants (
                id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
                name VARCHAR(200) NOT NULL,
                city_id INTEGER NOT NULL,
                FOREIGN KEY (city_id) REFERENCES cities(id)
                )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS foods (
                id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
                name VARCHAR(200),
                diets VARCHAR(100),
                date VARCHAR(20),
                lang VARCHAR(10),
                menu_type VARCHAR(100),
                menu_type_id INTEGER,
                created_at timestamp DEFAULT current_timestamp,
                restaurant_id INTEGER NOT NULL,
                FOREIGN KEY (restaurant_id) REFERENCES restaurants(id)
                )
        """)
        conn.commit()

    # menu_id INTEGER NOT NULL,
    # FOREIGN KEY (menu_id) REFERENCES menu(id)


# def create_table_alch(db):
#     Base = declarative_base()
#     Base.metadata.create_all(db)
#
#
# def insert_city_alch(Session, city):
#     with Session.begin() as session:
#         city = Cities(name=city)
#         session.add(city)


# def insert_restaurant_alch(Session, city_id, weekly_menu):
#     for item in weekly_menu:
#         restaurant_name = item['restaurant_name']
#         with Session.begin() as session:
#             restaurant = Restaurants(name=restaurant_name,
#                                      city_id=city_id)
#
#         for option in item['menu_options']:
#             food_name = option['food_name']
#             diets = option['diets']
#             date = option['date']
#             lang = option['lang']
#             menu_type = option['menu_type']
#             menu_type_id = option['menu_type_id']
#
#             with Session.begin() as session:
#                 restaurant = Foods(name=food_name,
#                                    diets=diets,
#                                    date=date,
#                                    lang=lang,
#                                    menu_type=menu_type_id)


def insert_city(city):
    conn_pg = psycopg.connect(db_string)
    with conn_pg as conn:

        # cursor.execute("SELECT id FROM cities WHERE name = ?", (city,))
        # result = cursor.fetchone()
        # if result:
        #     return result[0]

        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO cities (name)
            VALUES (%s)
            RETURNING id
        """, (city,))

        city_id, = cursor.fetchone()
        conn.commit()

    return city_id


def insert_restaurants(city_id, weekly_menu):
    conn_pg = psycopg.connect(db_string)
    with conn_pg as conn:
        for item in weekly_menu:
            restaurant_name = item['restaurant_name']

            cursor = conn.cursor()

            # cursor.execute("""SELECT id FROM restaurants
            #                WHERE name = ? AND city_id =?
            # """, (restaurant_name, city_id))
            # result = cursor.fetchone()
            # if result:
            #     restaurant_id = result[0]
            # else:

            cursor.execute("""
                INSERT INTO restaurants (name, city_id)
                VALUES (%s, %s)
                RETURNING id
            """, (restaurant_name, city_id))
            restaurant_id, = cursor.fetchone()
            conn.commit()

            # SELECT ?, ?
            # FROM restaurants r
            # WHERE EXISTS (select 1 FROM cities c WHERE c.id = r.city_id)

            for option in item['menu_options']:
                food_name = option['food_name']
                diets = option['diets']
                date = option['date']
                lang = option['lang']
                menu_type = option['menu_type']
                menu_type_id = option['menu_type_id']

                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO foods (name, diets, date, lang, menu_type, menu_type_id, restaurant_id)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (food_name,
                      diets,
                      date,
                      lang,
                      menu_type,
                      menu_type_id,
                      restaurant_id)
                )
                conn.commit()
