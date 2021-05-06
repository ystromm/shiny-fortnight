import io
import os

import boto3
from sanic import Sanic, json
from sanic.response import raw, empty


def server(s3):
    sanic = Sanic("api")

    @sanic.get("/healthcheck")
    async def healthcheck(request):
        return json({"status": "ok"})

    @sanic.get("/schema")
    async def list_schemas(request):
        list_objects_v2 = s3.list_objects_v2(bucket="schema_prod")
        keys = [list_object["Key"] for list_object in list_objects_v2["Contents"]]
        keys_without_json = [key_json[:-5] for key_json in keys]
        return json(keys_without_json)

    @sanic.get("/schema/<id>")
    async def get_schema(request, id):
        get_object = s3.get_object(Bucket="schema_prod", Key=id + ".json")
        body = get_object['Body'].read().decode('utf-8')
        return raw(body, content_type="application/json")

    @sanic.post("/schema/<id>")
    async def write_schema(request, id):

        stream = io.StringIO(request.body.decode('utf-8'))
        s3.upload_fileobj(stream, Bucket="schema_prod", Key=id + ".json")
        return empty(status=201)

    return sanic


if __name__ == "__main__":
    server(boto3.client("s3")).run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
