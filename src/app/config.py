import os

from dotenv import load_dotenv

load_dotenv()
if os.getenv("DB_URL"):
    db_url = os.getenv("DB_URL")
    db_string = db_url
else:
    db_type = os.getenv("DB_TYPE")
    db_user = os.getenv("DB_USER")
    db_name = os.getenv("DB_NAME")

    db_pass = os.getenv("DB_PASSWORD", "postgres")
    db_host = os.getenv("DB_HOST", "db")
    db_port = os.getenv("DB_PORT", "5432")

    if db_type == "postgresql":
        db_string = f"{db_type}://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
    else:
        db_string = f"dbname={db_name} user={db_user} host=db password={db_pass}"

# db_string = db_string

DEFAULT_CITY = "Tampere"
DATE_FORMAT = "%d.%m.%Y"
