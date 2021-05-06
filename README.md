#

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

```


## List files

requirements.txt:
```
boto3==1.17.*
```

Test:



