import psycopg

from psycopg.rows import dict_row

from core.config import db_string


def create_tables():
    conn_pg = psycopg.connect(db_string, row_factory=dict_row)
    with conn_pg as conn:

        cursor = conn.cursor()

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
                area VARCHAR(200) NOT NULL,
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
    conn_pg = psycopg.connect(db_string, row_factory=dict_row)
    with conn_pg as conn:
        for item in weekly_menu:
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
