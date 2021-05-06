SHELL=bash

venv: requirements-dev.txt
	(python3.8 -m venv venv && \
    . ./venv/bin/activate && \
    pip3 install -r requirements-dev.txt --extra-index-url https://pypi.fury.io/1ftg5H-EYOmJRWQKFg88FtE9aK1iF2Zjtw/funnel/)

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