-- migrate:up
CREATE TABLE IF NOT EXISTS cities (
    id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name TEXT NOT NULL UNIQUE,
    default_area TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS restaurants (
    id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name TEXT NOT NULL,
    area TEXT NOT NULL,
    city_id INTEGER REFERENCES cities(id)
);

CREATE TABLE IF NOT EXISTS foods (
    id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name TEXT,
    diets TEXT,
    menu_type TEXT,
    menu_uid INTEGER,
    date DATE, -- or text
    lang TEXT,
    created_at timestamp DEFAULT current_timestamp,
    restaurant_id INTEGER REFERENCES restaurants(id)
);

-- migrate:down
