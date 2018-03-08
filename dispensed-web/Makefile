PACKAGE_NAME = Dispensed Web
SHELL = /bin/bash

default:
	( \
    python3 -m venv venv; \
	  source venv/bin/activate; \
	  pip install -r requirements.txt; \
	)

check:
	( \
		source venv/bin/activate; \
		pip install --upgrade --requirement=requirements-check.txt; \
		echo "Running Code check!"; \
		flake8 --ignore D100,D101,D102,D103,D104,D105 \
					--exclude .git,__pycache__,venv,migrations,docs,app/__init__.py; \
	)

clean:
	@rm -Rf *.egg .cache .coverage .tox build dist docs/build htmlcov
	@find -depth -type d -name __pycache__ -exec rm -Rf {} \;
	@find -type f -name '*.pyc' -delete
