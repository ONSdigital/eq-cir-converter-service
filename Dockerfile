FROM python:3.12.6

WORKDIR /app

COPY pyproject.toml poetry.lock /app/

RUN pip install --no-cache-dir poetry==1.8.4 && \
    poetry config virtualenvs.in-project true && \
    poetry install --no-root --no-dev

COPY . /app

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "5010"]