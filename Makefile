.PHONY: install
install:
	poetry install

.PHONY: migrate
migrate:
	poetry run python -m cooking_core.manage migrate

.PHONY: migrations
migrations:
	poetry run python -m cooking_core.manage makemigrations

.PHONY: run-server
run-server:
	poetry run python -m cooking_core.manage runserver

.PHONY: superuser
superuser:
	poetry run python -m cooking_core.manage createsuperuser

.PHONY: update
update: install migrate ;
