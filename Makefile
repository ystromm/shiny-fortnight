SHELL=bash

venv: requirements-dev.txt
	(python3.8 -m venv venv && \
    . ./venv/bin/activate && \
    pip3 install -r requirements-dev.txt)

setup: venv

.PHONY: test
test: setup
	@ . venv/bin/activate && PYTHONPATH=src pytest test && flake8 src --exclude '#*,~*,.#*'

clean:
	rm -rf venv
	rm -rf dist
	rm -rf __pycache__
	rm -f *.pyc
	rm -rf src/settings.py%