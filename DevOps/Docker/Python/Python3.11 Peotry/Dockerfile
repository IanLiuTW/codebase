# Specify the variables
ARG SRC_DIR=src


FROM python:3.11.4-alpine3.18 as base

FROM base as poetry
WORKDIR /app
# Install poetry and use it to export requirements.txt
RUN pip install poetry
COPY pyproject.toml poetry.lock ./
RUN poetry export -f requirements.txt --output requirements.txt

FROM base as app
WORKDIR /app
# Install basic build tools and dependencies packages
# RUN apk add --no-cache build-base git bash
# RUN ...
COPY --from=poetry /app/requirements.txt .
RUN pip install -r requirements.txt
# Copy the source code and run the app
COPY ./$SRC_DIR ./$SRC_DIR
CMD python $SRC_DIR/main.py
