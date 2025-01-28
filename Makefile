.DEFAULT_GOAL := all

.PHONY: all
all: ## Show the available make targets.
	@echo "Usage: make <target>"
	@echo ""
	@echo "Targets:"
	@fgrep "##" Makefile | fgrep -v fgrep

.PHONY: clean
clean: ## Clean the temporary files.
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf .coverage
	rm -rf .ruff_cache
	rm -rf megalinter-reports

.PHONY: format
format:  ## Format the code.
	poetry run black .
	poetry run ruff check . --fix

.PHONY: lint
lint:  ## Run all linters (black/ruff/pylint/mypy).
	poetry run black --check .
	poetry run ruff check .
	make mypy

.PHONY: test
test:  ## Run the tests and check coverage.
	poetry run pytest -n auto --cov=eq_cir_converter_service --cov-report term-missing --cov-fail-under=100

.PHONY: mypy
mypy:  ## Run mypy.
	poetry run mypy -p eq_cir_converter_service

.PHONY: install
install:  ## Install the dependencies excluding dev.
	poetry install --only main

.PHONY: install-dev
install-dev:  ## Install the dependencies including dev.
	poetry install

.PHONY: megalint
megalint:  ## Run the mega-linter.
	docker run --platform linux/amd64 --rm \
		-v /var/run/docker.sock:/var/run/docker.sock:rw \
		-v $(shell pwd):/tmp/lint:rw \
		oxsecurity/megalinter:v7

.PHONY: run
run:  ## Start the local application.
	poetry run uvicorn eq_cir_converter_service.app.main:app --reload --port 5010

.PHONY: docker-build
docker-build:  ## Build the docker image.
	docker build -t cir-converter-service .

.PHONY: docker-compose-up
docker-compose-up:  ## Start the docker container using docker-compose.
	docker compose up --build -d

.PHONY: docker-compose-down
docker-compose-down:  ## Stop the docker container using docker-compose.
	docker compose down