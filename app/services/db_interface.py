import sqlite3
from datetime import datetime


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

    # Very dirty solution > need to come up with better one
    cursor.execute("DROP TABLE IF EXISTS foods")
    cursor.execute("DROP TABLE IF EXISTS restaurants")
    cursor.execute("DROP TABLE IF EXISTS cities")

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


def insert_city(conn, city):
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO cities (name)
        VALUES (?)
    """, (city,))
    conn.commit()

    city_id = cursor.lastrowid
    return city_id


def insert_restaurants(conn, city_id, weekly_menu):
    cursor = conn.cursor()
    for item in weekly_menu:
        restaurant_name = item['restaurant_name']

        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO restaurants (name, city_id)
            VALUES (?, ?)
        """, (restaurant_name, city_id))
        restaurant_id = cursor.lastrowid
        conn.commit()

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
