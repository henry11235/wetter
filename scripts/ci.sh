#!/bin/bash

poetry run flake8 src/
poetry run black --check src/
poetry run isort --check-only src/
poetry run mypy src/
poetry run pytest --cov=src tests/
