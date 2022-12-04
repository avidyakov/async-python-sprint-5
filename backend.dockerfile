FROM python:3.11.0

WORKDIR /app/
ENV PYTHONPATH=/app
EXPOSE 8000

RUN pip install poetry && poetry config virtualenvs.create false

COPY ./pyproject.toml ./poetry.lock* ./
RUN poetry install --no-root --no-interaction --no-ansi --no-cache

COPY ./ ./
CMD ["python", "src/main.py"]
