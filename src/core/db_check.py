import psycopg
import os

from psycopg.rows import dict_row
from core.config import db_string

conn = psycopg.connect(db_string, row_factory=dict_row)
ispopulated = ''
with conn:
    ispopulated = conn.execute('''
            SELECT EXISTS (
            SELECT 1 FROM pg_tables
            WHERE schemaname = 'public'
            )
            ''').fetchone()

if not ispopulated['exists']:
    # breakpoint()
    os.system('uv run src/webscraper/engine.py')
