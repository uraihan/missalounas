import sqlite3
from datetime import datetime
# from sqlalchemy import create_engine, Column, Integer, String, Text

# NOTE: database schema
# Table City {
#   id int pk
#   name varchar
#   restaurantid int
# }
#
# Table Restaurant {
#   id int pk
#   name varchar
#   openingHours varchar
#   cityid int
# }
#
# Table Menu {
#   id int pk
#   createAt datetime
#   day varchar
#   menuType varchar -> lounas/vegan
#   lang varchar
#   restaurantid int
# }
#
# Table Food {
#   id int pk
#   createAt datetime
#   day varchar
#   menuType varchar -> lounas/vegan
#   name varchar
#   diets varchar
#   lang varchar
#   menuid int
# }
# Ref: Restaurant.cityid > City.restaurantid
#
# Ref: Restaurant.id < Menu.restaurantid
#
# Ref: Menu.id < Food.menuid


def create_tables(conn):
    cursor = conn.cursor()

    cursor.execute("PRAGMA foreign_keys = ON")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(200) NOT NULL UNIQUE
            )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS restaurants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(200) NOT NULL,
            city_id INTEGER NOT NULL,
            FOREIGN KEY (city_id) REFERENCES cities(id)
            )
    """)
    # opening_hours VARCHAR(200),

    # cursor.execute("""
    #     CREATE TABLE IF NOT EXISTS menus (
    #         id INTEGER PRIMARY KEY AUTOINCREMENT,
    #         created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    #         date VARCHAR(20),
    #         lang VARCHAR(10),
    #         menu_type VARCHAR(100),
    #         restaurant_id INTEGER NOT NULL,
    #         FOREIGN KEY (restaurant_id) REFERENCES restaurant(id)
    #         )
    # """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS foods (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(200),
            diets VARCHAR(100),
            date VARCHAR(20),
            lang VARCHAR(10),
            menu_type VARCHAR(100),
            menu_type_id INTEGER,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            restaurant_id INTEGER NOT NULL,
            FOREIGN KEY (restaurant_id) REFERENCES restaurants(id)
            )
    """)
    conn.commit()
    # menu_id INTEGER NOT NULL,
    # FOREIGN KEY (menu_id) REFERENCES menu(id)


def insert_city(conn, city):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO cities (name)
        VALUES (?)
    """, (city,))
    city_id = cursor.lastrowid

    return city_id


def insert_restaurants(conn, city_id, weekly_menu):
    cursor = conn.cursor()
    for item in weekly_menu:
        restaurant_name = item['restaurant_name']

        cursor.execute("""
            INSERT INTO restaurants (name, city_id)
            VALUES (?, ?)
        """, (restaurant_name, city_id))
        restaurant_id = cursor.lastrowid

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
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (food_name, diets, date, lang, menu_type, menu_type_id,
                  restaurant_id))

    conn.commit()


# def insert_foods(conn, restaurant_id, food_name, diets, date, menu_type,
#                  menu_type_id, lang):

    # cursor.execute("""
    #     INSERT INTO restaurants (id, name, city_id)
    #     VALUES (?, ?, ?, ?)
    # """, (restaurant_id, restaurant_name, city_id))
    #
    # for day in response['days']:
    #     date = day['date']
    #     cursor.execute("""
    #         INSERT INTO menus (created_at, date, menu_type, lang, restaurant_id)
    #         VALUES (?, ?, ?, ?, ?)
    #     """, (created_at, date, ))
