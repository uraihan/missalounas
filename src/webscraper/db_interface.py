import psycopg

from psycopg.rows import dict_row

from app.config import db_string


def create_tables():
    conn_pg = psycopg.connect(db_string, row_factory=dict_row)
    with conn_pg as conn:

        cursor = conn.cursor()

        # Very dirty solution > need to come up with better one
        cursor.execute("DROP TABLE IF EXISTS cities CASCADE")
        cursor.execute("DROP TABLE IF EXISTS foods CASCADE")
        cursor.execute("DROP TABLE IF EXISTS restaurants CASCADE")

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
                area VARCHAR(200) NOT NULL,
                city_id INTEGER REFERENCES cities(id)
                )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS foods (
                id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
                name VARCHAR(200),
                diets VARCHAR(100),
                menu_type VARCHAR(200),
                menu_uid INTEGER,
                date VARCHAR(20),
                lang VARCHAR(10),
                created_at timestamp DEFAULT current_timestamp,
                restaurant_id INTEGER REFERENCES restaurants(id)
                )
        """)
        conn.commit()


def insert_city(city):
    conn_pg = psycopg.connect(db_string, row_factory=dict_row)
    with conn_pg as conn:

        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO cities (name)
            VALUES (%s)
            RETURNING id
        """, (city,))

        city_id = cursor.fetchone()['id']
        conn.commit()

    return city_id


def insert_restaurants(city_id, weekly_menu):
    for item in weekly_menu:
        conn_pg = psycopg.connect(db_string, row_factory=dict_row)
        with conn_pg as conn:
            restaurant_name = item['restaurant_name']
            area_name = item['area']

            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO restaurants (name, area, city_id)
                VALUES (%s, %s, %s)
                RETURNING id
            """, (restaurant_name, area_name, city_id))
            restaurant_id = cursor.fetchone()['id']
            conn.commit()

        for food in item['menu_options']:
            conn_pg = psycopg.connect(db_string, row_factory=dict_row)
            with conn_pg as conn:
                food_name = food.get('food_name')
                diets = food.get('diets')
                menu_type = food.get('menu_type')
                menu_uid = food.get('menu_uid')
                date = food.get('date')
                lang = food.get('lang')

                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO foods (name, diets, menu_type, menu_uid, date, lang, restaurant_id)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (food_name,
                      diets,
                      menu_type,
                      menu_uid,
                      date,
                      lang,
                      restaurant_id)
                )
                conn.commit()
