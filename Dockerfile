FROM python:3.12.6-alpine

WORKDIR /eq_cir_converter_service

COPY pyproject.toml poetry.lock /eq_cir_converter_service/

RUN pip install --no-cache-dir poetry==1.8.4 && \
    poetry config virtualenvs.create false && \
    poetry install --no-root --no-dev

COPY eq_cir_converter_service eq_cir_converter_service

ENV LOG_LEVEL=INFO

# Create a non-root user and group
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

# Change ownership of the application directory to the non-root user
RUN chown -R appuser:appgroup /eq_cir_converter_service

# Set the user running the application to the non-root user
USER appuser

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:5010/docs || exit 1

CMD ["uvicorn", "eq_cir_converter_service.main:app", "--host", "0.0.0.0", "--port", "5010"]
