# NOTE: this was part of the webscraper/ dir
#
import psycopg
from psycopg import Connection
from psycopg.rows import DictRow, dict_row

from src.shared.config import get_db_string


def init_db() -> Connection[DictRow]:
    return Connection[DictRow].connect(conninfo=get_db_string(), row_factory=dict_row)


# NOTE: DEPRECATED
def create_tables():
    db_string = get_db_string()
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
                name VARCHAR NOT NULL UNIQUE
                )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS restaurants (
                id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
                name VARCHAR NOT NULL,
                area VARCHAR NOT NULL,
                city_id INTEGER REFERENCES cities(id)
                )
        """)  # name column: candidate for unique constraint

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS foods (
                id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
                name VARCHAR,
                diets VARCHAR,
                menu_type VARCHAR,
                menu_uid INTEGER,
                date VARCHAR,
                lang VARCHAR,
                created_at timestamp DEFAULT current_timestamp,
                restaurant_id INTEGER REFERENCES restaurants(id)
                )
        """)
        conn.commit()


def insert_city(city: str, db: psycopg.Connection):
    row = db.execute(
        """
        INSERT INTO cities (name)
        VALUES (%s)
        ON CONFLICT (name) DO NOTHING
        RETURNING id
    """,
        (city,),
    ).fetchone()

    if row:
        city_id = row.get("id")
    else:
        city_id = db.execute(
            "SELECT id FROM cities WHERE name = %s", (city,)
        ).fetchone()
        city_id = city_id.get("id")
    db.commit()

    return city_id


def insert_restaurants(city_id: int, weekly_menu, db: psycopg.Connection):
    for item in weekly_menu:
        restaurant_name = item["restaurant_name"]
        area_name = item["area"]

        check_rest = db.execute(
            """
            SELECT id from restaurants
            WHERE name = %s
        """,
            (restaurant_name,),
        ).fetchone()

        if check_rest:
            restaurant_id = check_rest.get("id")
        else:
            restaurant_id = db.execute(
                """
                INSERT INTO restaurants (name, area, city_id)
                VALUES (%s, %s, %s)
                RETURNING id
            """,
                (restaurant_name, area_name, city_id),
            ).fetchone()
            restaurant_id = restaurant_id.get("id")
        db.commit()

        try:
            for food in item["menu_options"]:
                food_name = food.get("food_name")
                diets = food.get("diets")
                menu_type = food.get("menu_type")
                menu_uid = food.get("menu_uid")
                date = food.get("date")
                lang = food.get("lang")

                # update food instead of making new if food id changes
                db.execute(
                    """
                    INSERT INTO foods (name, diets, menu_type, menu_uid, date, lang, restaurant_id)
                    SELECT %s, %s, %s, %s, %s, %s, %s
                    WHERE NOT EXISTS (
                        SELECT name FROM foods
                        WHERE name = %s AND date = %s AND menu_uid = %s
                        AND restaurant_id = %s AND lang = %s
                    )
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
                        menu_uid,
                        restaurant_id,
                        lang,
                    ),
                )
            db.commit()
        except psycopg.Error as e:
            db.rollback()
            print(f"Failed to insert foods for {restaurant_name}: {e}")
            continue
