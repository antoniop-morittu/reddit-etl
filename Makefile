PACKAGE = package/reddit-api/src/reddit_api

install:
	pip install --upgrade pip &&\
		pip install -r requirements-dev.txt\
		pip install -e package/reddit-api

custom:
	rm -rf dags/custom/*
	cp -rf package/reddit-api/src/reddit_api/* dags/custom/

test:
	#python -m pytest -vv --cov=api --cov=etl test_*.py

format:	
	black dags/*.py $(PACKAGE)/*.py main.py

lint:
	- pylint --disable=R,C --ignore-patterns=test_.*?py --ignore-patterns=dags/*?py $(PACKAGE)/*.py main.py

container-lint:
	- docker run --rm -i hadolint/hadolint < docker/airflow-data/Dockerfile

refactor: format lint
		
all: install lint test format