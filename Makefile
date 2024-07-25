install:
	pip3 install poetry
	poetry install

run:
	python3 flask_ticket_system/entrypoints/flaskapp/app.py

shell:
	poetry shell

build-docker:
	docker build -t flask_ticket_system .

run-docker:
	docker run -p 80:80 flask_ticket_system
