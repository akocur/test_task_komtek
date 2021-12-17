MANAGE := poetry run python manage.py

install:
	poetry install
test:
	poetry run pytest -vv
test-django:
	@$(MANAGE) test
test-coverage:
	poetry run pytest --cov=terminology
code-climate:
	poetry run pytest --cov=terminology --cov-report xml
lint:
	poetry run flake8
selfcheck:
	poetry check
check: selfcheck test lint

build: check
	poetry build

rec:
	poetry run asciinema rec

install-package: build
	python3 -m pip install --user .

.PHONY: makemigrations
makemigrations:
	@$(MANAGE) makemigrations

.PHONY: migrate
migrate: makemigrations
	@$(MANAGE) migrate

.PHONY: shell
shell:
	@$(MANAGE) shell_plus --ipython

run:
	@$(MANAGE) runserver

.PHONY: install test lint selfcheck check build