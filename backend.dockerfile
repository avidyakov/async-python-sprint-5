FROM python:3.11-alpine

WORKDIR /app/
ENV PYTHONPATH=/app
EXPOSE 8000

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

COPY ./pyproject.toml ./poetry.lock* ./
RUN poetry install --no-root --no-dev

COPY ./ ./
