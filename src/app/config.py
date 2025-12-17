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
    db_string = f"dbname={db_name} user={db_user} host='localhost'"

    if os.getenv("DB_PASSWORD"):
        db_pass = os.getenv("DB_PASSWORD")
        db_string += f" password={db_pass}"

db_string = db_string

DEFAULT_CITY = "Tampere"
DATE_FORMAT = "%d.%m.%Y"
PH_SECRETS = os.getenv("PH_SECRETS")
