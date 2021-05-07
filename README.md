# shiny-forthnight

Build a simple API using and S3 bucket as the storage.

##

Makefile:

````makefile

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

```
curl localhost:8080/healthcheck
{"status":"ok"}
```

A test:

```
...
```

Factory function to create server:

```
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



