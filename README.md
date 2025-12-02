# Missä Lounas?
Compare menus across Finnish student restaurants in one place.

**This is a Work in Progress. To-Dos:**
- [x] APIs routing and interaction with database (Flask/FastAPI)
- [x] Web frontend
- [ ] Dockerfile (or find out if I even need it)

## Development
This project used uv to manage Python dependencies and virtual environment. To start the web scraping engine, run:
```
uv run app/services/engine.py
```

This will make GET requests to API endpoints of student restaurant chains, parse
them up, and store in a SQLite database.

To fire up the Flask web server, run:
```
flask --app main run
```
