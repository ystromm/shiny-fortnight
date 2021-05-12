# shiny-forthnight

Build a simple API using and S3 bucket as the storage.

## Some basic stuff

Makefile:

````makefile
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
````

requirements.txt: 

````text
sanic==21.*
````

requirements-dev.txt: 

````text
-r requirements.txt
sanic-testing==0.3.*
pytest
````

## Healthcheck

Let's the load balancer know that the API instance is up and running.

```shell script
curl localhost:8080/healthcheck
{"status":"ok"}
```

A test for health check.
test/test_server.py:

```python
def test_get_healtcheck_returns_200():
    server_under_test = server_factory()
    TestManager(server_under_test)
    request, response = server_under_test.test_client.get('/healthcheck')
    assert response.status == 200
```

Setup method to create a test server:
test/test_server.py:

```python
def server_factory():
    server_under_test = server()
    TestManager(server_under_test)
    return server_under_test
```

Implementation in src/server.py.
Create the server in a factory method. 

```python
from sanic import Sanic, json

def server():
    sanic = Sanic("api")

    @sanic.get("/healthcheck")
    async def healthcheck(request):
        return json({"alive": "kicking"})
```

Entry point: 

```python
if __name__ == "__main__":
    server().run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
```

## List files

requirements.txt:
```
boto3==1.17.*
```

Test:

```
...
```

## Get a single file

Test:

```
...
```

## Upload and validate

```sh
curl --XPUT localhost:8080/schema/test?validate=true -D ...
```
Test:
```
...
```

JSON schema:

```
```

requirements.txt:
```
jsonschema==3.2.0
```



