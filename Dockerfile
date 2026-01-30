#### BUILDING TAILWIND CSS #####
FROM node:20-trixie-slim AS tailwind-builder

WORKDIR /node

# Copy nodejs dependency
COPY package*.json /node/

# Install nodejs dependency
RUN npm install

# Copy necessary Tailwind CSS files to generate main.css
COPY ./static/daisy.css /node/static/
COPY templates/ ./templates/

RUN npx @tailwindcss/cli -i ./static/daisy.css -o ./static/main.css --minify

##### BUILDING PYTHON #####
FROM python:3.12-slim-trixie AS app

WORKDIR /app

RUN apt-get update && apt-get install -y curl locales \
    # postgresql-client \
    && rm -rf /var/lib/apt/lists/*

RUN sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
    sed -i -e 's/# fi_FI.UTF-8 UTF-8/fi_FI.UTF-8 UTF-8/' /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY . /app/

RUN uv sync --locked
RUN mkdir -p log/

COPY --from=tailwind-builder /node/static/main.css /app/static/

EXPOSE 8080

RUN chmod +x /app/start.sh

CMD ["/app/start.sh"]
