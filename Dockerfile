FROM python:3.12.6-slim

WORKDIR /app

COPY pyproject.toml poetry.lock /app/

RUN pip install --no-cache-dir poetry==1.8.4 && \
    poetry config virtualenvs.create false && \
    poetry install --no-root --no-dev

COPY eq_cir_converter_service/app eq_cir_converter_service/app

ENV PYTHONPATH=eq_cir_converter_service/app

CMD ["uvicorn", "eq_cir_converter_service.app.main:app", "--host", "0.0.0.0", "--port", "5010"]