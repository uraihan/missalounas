#### BUILDING TAILWIND CSS #####
FROM node:20-alpine AS tailwind-builder

WORKDIR /app

# Copy nodejs dependency
COPY package*.json ./

# Install nodejs dependency
RUN npm install

# Copy necessary Tailwind CSS files to generate main.css
COPY static/daisy.css ./static/
COPY templates/ ./templates/

RUN npx @tailwindcss/cli -i ./static/daisy.css -o ./static/main.css --minify

##### BUILDING PYTHON #####
FROM python:3.12-slim-trixie
WORKDIR /app

RUN apt-get update && apt-get install -y \
    curl locales \
    # postgresql-client \
    && rm -rf /var/lib/apt/lists/*

RUN sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
    sed -i -e 's/# fi_FI.UTF-8 UTF-8/fi_FI.UTF-8 UTF-8/' /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY . /app

RUN uv sync --locked --no-dev --no-install-project
RUN uv sync --locked --no-dev --no-editable
RUN mkdir -p log/

COPY . .

COPY --from=tailwind-builder /app/static/main.css ./static/main.css

RUN echo '#!/bin/bash\n\
set -e\n\
source /app/.venv/bin/activate\n\
echo "Checking database..."\n\
uv run src/app/db_check.py\n\
echo "Starting Gunicorn server..."\n\
exec gunicorn --bind 0.0.0.0:$PORT --timeout 120 --access-logfile - main:app\n\
' > /app/start.sh && chmod +x /app/start.sh

EXPOSE 8080

CMD ["/app/start.sh"]
