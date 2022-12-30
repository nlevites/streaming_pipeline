PYTHON_CMD ?= python

requirements.txt: requirements.in
	pip-compile --no-emit-index-url --resolver=backtracking --output-file=requirements.txt requirements.in

requirements-dev.txt: requirements-dev.in
	pip-compile --no-emit-index-url --resolver=backtracking --output-file=requirements-dev.txt requirements-dev.in

create-virtualenv:
	python3.9 -m venv ./venv
	venv/bin/pip install -r requirements-dev.txt --no-dependencies

create-virtualenv-parallel-download:
	python3.9 -m venv ./venv
	grep -h "==" requirements.txt requirements-dev.txt | xargs -t -n1 -P8 venv/bin/pip download --no-deps -d ./dist
	venv/bin/pip install --no-deps --no-index --find-links="./dist" -r requirements.txt -r requirements-dev.txt

install-requirements:
	${PYTHON_CMD} -m pip install -r requirements.txt
	${PYTHON_CMD} -m pip install -r requirements-dev.txt

sort-imports:
	${PYTHON_CMD} -m isort --profile black .

check-security:
	${PYTHON_CMD} -m bandit .

lint-flake8:
	${PYTHON_CMD} -m flake8 --exclude=venv .

lint-black:
	${PYTHON_CMD} -m black --check --diff .

check-types:
	${PYTHON_CMD} -m mypy --ignore-missing-imports --follow-imports=silent --strict --allow-any-generics api/

run-unit-tests:
	${PYTHON_CMD} -m pytest -v --cov=validator --cov-report=term-missing tests/

all-checks: sort-imports lint-black lint-flake8 check-types check-security run-unit-tests
