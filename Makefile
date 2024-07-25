install:
	pip3 install poetry
	poetry install

run:
	python3 flask_ticket_system/entrypoints/flaskapp/app.py

shell:
	poetry shell
