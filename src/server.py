import io
import os

import boto3
from sanic import Sanic, json
from sanic.response import raw, empty

BUCKET = "shiny-forthnight"


def server(s3):
    app = Sanic("api")

    @app.get("/healthcheck")
    async def healthcheck(request):
        return json({"status": "ok"})

    @app.get("/schema")
    async def list_schemas(request):
        list_objects_v2 = s3.list_objects_v2(Bucket=BUCKET)
        keys = [list_object["Key"] for list_object in list_objects_v2["Contents"]]
        keys_without_json = [key_json[:-5] for key_json in keys]
        return json(keys_without_json)

    @app.get("/schema/<id>")
    async def get_schema(request, id):
        get_object = s3.get_object(Bucket=BUCKET, Key=id + ".json")
        body = get_object['Body'].read()
        return raw(body, content_type="application/json", headers={"content-encoding": "gzip"})

    return app


if __name__ == "__main__":
    server(boto3.client("s3")).go_fast(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
