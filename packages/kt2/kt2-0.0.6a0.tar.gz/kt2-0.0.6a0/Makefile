.PHONY: setup_venv install_pipelines install-dev flake8 lint format test shell docsgen

setup_venv:
	python -m venv ./venv/

install_pipelines: setup_venv
	./venv/bin/python -m pip install -U pip
	./venv/bin/python -m pip install -r requirements.txt
	./venv/bin/python -m pip install '.[dev]'

install-dev:
	pip install '.[dev]'
	pip install '.[doc]'

flake8:
	flake8 koppeltaal

ruff:
	ruff koppeltaal

lint:
	./scripts/lint.sh

format:
	./scripts/format.sh

release:
	./scripts/release.sh

test:
	./scripts/test-integration.sh

shell:
	ipython

docsgen:
	pdoc3 -f --skip-errors --html -o docs koppeltaal