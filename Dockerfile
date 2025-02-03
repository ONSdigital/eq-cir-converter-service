FROM python:3.12.6-alpine

WORKDIR /eq_cir_converter_service

COPY pyproject.toml poetry.lock /eq_cir_converter_service/

RUN pip install --no-cache-dir poetry==1.8.4 && \
    poetry config virtualenvs.create false && \
    poetry install --no-root --no-dev

COPY eq_cir_converter_service eq_cir_converter_service

CMD ["uvicorn", "eq_cir_converter_service.main:app", "--host", "0.0.0.0", "--port", "5010"]