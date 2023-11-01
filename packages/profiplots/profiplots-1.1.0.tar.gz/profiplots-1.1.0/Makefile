SHELL = /bin/bash
PYTHON ?= python


install_dev:
	$(PYTHON) -m pip install -r requirements-ci.txt -e .
	$(PYTHON) -m pre_commit install

compile:
	$(PYTHON) -m piptools compile --resolver=backtracking --no-emit-index-url -o requirements.txt pyproject.toml
	$(PYTHON) -m piptools compile --resolver=backtracking --no-emit-index-url --extra=ci -o requirements-ci.txt pyproject.toml
	$(PYTHON) -m piptools compile --resolver=backtracking --no-emit-index-url --extra=docs -o requirements-docs.txt pyproject.toml

sync:
	$(PYTHON) -m piptools sync requirements-ci.txt
	$(PYTHON) -m pip install -e .

up: compile sync

docs:
	cd docs/ && $(PYTHON) -m quartodoc build && quarto render

clean:
	find . -type d -name .pytest_cache | xargs --no-run-if-empty -t rm -r
	find . -type d -name __pycache__ | xargs --no-run-if-empty -t rm -r
	find . -type d -name dist | xargs --no-run-if-empty -t rm -r
	find . -type d -name build | xargs --no-run-if-empty -t rm -r
	find . -type d -regex ".*\.egg.*"  | xargs --no-run-if-empty -t rm -r
	rm -rf docs/_site docs/_freeze docs/.quarto docs/api docs/site_libs docs/objects.json

.PHONY: install_dev compile sync up docs clean
