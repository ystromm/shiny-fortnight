# shiny-forthnight

Build a simple API using an S3 bucket as the storage.

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
	@ . venv/bin/activate && PYTHONPATH=src pytest test'

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
    return server_under_test
```

Implementation in src/server.py.
Create the server in a factory method. 

```python
from sanic import Sanic, json

def server():
    app = Sanic("api")

    @app.get("/healthcheck")
    async def healthcheck(request):
        return json({"status": "ok"})
    
    return app
```

Entry point: 

```python
if __name__ == "__main__":
    server().run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
```

## List files

Let's start with a test:

````python
def test_get_schema_returns_empty_list():
    server_under_test = server_factory()
    request, response = server_under_test.test_client.get('/schema')
    assert response.status == 200
    assert response.json == []
````

And the naive implementation:

````python
    @app.get("/schema")
    async def list_schemas(request):
        return json([])
````

To do a real implementation we need a boto3 client:

requirements.txt:

```text
boto3==1.17.*
```

Get schemas should call list_objects:

```python
def test_get_schema_should_list_objects():
    server_under_test, s3 = server_factory()
    request, response = server_under_test.test_client.get('/schema')
    s3.list_objects_v2.assert_called_with(Bucket="shiny-forthnight")
    assert response.status == 200
```

To allow for tests we need to add the s3 client as a parameter:

```python
from unittest.mock import MagicMock

def server_factory():
    s3 = MagicMock()
    server_under_test = server(s3)
    TestManager(server_under_test)
    return server_under_test, s3
```

Update factory method and entry point:

```python
BUCKET="shiny-forthnight"

def server(s3):

    @app.get("/schema")
    async def list_schemas(request):
        list_objects_v2 = s3.list_objects_v2(Bucket="BUCKET)
        return json([])

if __name__ == "__main__":
    server(boto3.client("s3")).run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
```

Test to simulate actual data:

```python
def test_get_schema_should_list_objects():
    server_under_test, s3 = server_factory()
    s3.list_objects_v2.return_value = {
        'Contents': [
            {
                'Key': 'a.json'
            },
            {
                'Key': 'b.json'
            }
        ]
    }
    request, response = server_under_test.test_client.get('/schema')
    s3.list_objects_v2.assert_called_with(Bucket="shiny-forthnight")
    assert response.status == 200
    assert response.json == ["a", "b"]
```

And transform the response:

```python
    @app.get("/schema")
    async def list_schemas(request):
        list_objects_v2 = s3.list_objects_v2(Bucket=BUCKET)
        keys = [list_object["Key"] for list_object in list_objects_v2["Contents"]]
        keys_without_json = [key_json[:-5] for key_json in keys]
        return json(keys_without_json)
```

What about files with other extensions? 

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

## Deploy

Dockerfile:

```docker
FROM python:3.8
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY src .
CMD python3 server.py
```

Makefile:
```
 .PHONY: build
build:
	docker build --tag shiny-forthnight .
```

```shell
docker run -p8080:8080 shiny-forthnight
```



## openapi

requirements.txt:
```
sanic-openapi==21.*
```

server.py:
```

```





