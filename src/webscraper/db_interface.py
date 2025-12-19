import psycopg

from psycopg.rows import dict_row

from app.config import db_string


def create_tables():
    conn_pg = psycopg.connect(db_string, row_factory=dict_row)
    with conn_pg as conn:
        cursor = conn.cursor()

        # Very dirty solution > need to come up with better one
        # cursor.execute("DROP TABLE IF EXISTS cities CASCADE")
        # cursor.execute("DROP TABLE IF EXISTS foods CASCADE")
        # cursor.execute("DROP TABLE IF EXISTS restaurants CASCADE")

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
        """)  # name column: candidate for unique constraint

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
        cursor.execute(
            """
            INSERT INTO cities (name)
            VALUES (%s)
            ON CONFLICT (name) DO NOTHING
            RETURNING id
        """,
            (city,),
        )

        row = cursor.fetchone()
        if row:
            city_id = row.get("id")
        else:
            cursor.execute("SELECT id FROM cities WHERE name = %s", (city,))
            city_id = cursor.fetchone().get("id")
        conn.commit()

    return city_id


def insert_restaurants(city_id, weekly_menu):
    for item in weekly_menu:
        conn_pg = psycopg.connect(db_string, row_factory=dict_row)
        with conn_pg as conn:
            restaurant_name = item["restaurant_name"]
            area_name = item["area"]

            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT id from restaurants
                WHERE name = %s
            """,
                (restaurant_name,),
            )
            check_rest = cursor.fetchone()

            if check_rest:
                restaurant_id = check_rest.get("id")
            else:
                cursor.execute(
                    """
                    INSERT INTO restaurants (name, area, city_id)
                    VALUES (%s, %s, %s)
                    RETURNING id
                """,
                    (restaurant_name, area_name, city_id),
                )
                restaurant_id = cursor.fetchone().get("id")
            conn.commit()

        for food in item["menu_options"]:
            conn_pg = psycopg.connect(db_string, row_factory=dict_row)
            with conn_pg as conn:
                food_name = food.get("food_name")
                diets = food.get("diets")
                menu_type = food.get("menu_type")
                menu_uid = food.get("menu_uid")
                date = food.get("date")
                lang = food.get("lang")

                # update food instead of making new if food id changes
                cursor = conn.cursor()
                cursor.execute(
                    """
                    INSERT INTO foods (name, diets, menu_type, menu_uid, date, lang, restaurant_id)
                    SELECT %s, %s, %s, %s, %s, %s, %s
                    WHERE NOT EXISTS (
                        SELECT name FROM foods
                        WHERE name = %s AND date = %s
                    )
                    RETURNING id
                """,
                    (
                        food_name,
                        diets,
                        menu_type,
                        menu_uid,
                        date,
                        lang,
                        restaurant_id,
                        food_name,
                        date,
                    ),
                )
                # cursor.execute("""
                #     SELECT id from foods
                #     WHERE name = %s AND date = %s AND lang = %s
                # """, (food_name, date, lang))
                # check_menu = cursor.fetchone()
                # if check_menu:
                #     pass
                # else:
                #     cursor.execute("""
                #         INSERT INTO foods (name, diets, menu_type, menu_uid, date, lang, restaurant_id)
                #         VALUES (%s, %s, %s, %s, %s, %s, %s)
                #     """, (food_name,
                #           diets,
                #           menu_type,
                #           menu_uid,
                #           date,
                #           lang,
                #           restaurant_id)
                #     )
                conn.commit()
