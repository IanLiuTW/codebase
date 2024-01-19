FROM python:3.11.4-alpine3.18 as base

FROM base as poetry
WORKDIR /app
# Install poetry and use it to export requirements.txt
RUN pip install poetry
COPY pyproject.toml poetry.lock ./
RUN poetry export --without-hashes -f requirements.txt --output requirements.txt

FROM base as app
WORKDIR /app
# Install basic build tools and dependencies packages
# RUN apk add --no-cache build-base git bash
# RUN ...
COPY --from=poetry /app/requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
# Copy the source code and run the app
COPY ./src ./src
CMD python src/main.py
