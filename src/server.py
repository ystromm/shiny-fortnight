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
        list_objects_v2 = s3.list_objects_v2(Bucket="funnel-data-schema-stage")
        keys = [list_object["Key"] for list_object in list_objects_v2["Contents"]]
        keys_without_json = [key_json[:-5] for key_json in keys]
        return json(keys_without_json)

    # {'ResponseMetadata': {'RequestId': '8QN5K10WMX2ZG2ZS', 'HostId': 'w1o+46zTKSTJ9bdekbzU2a6zfQd2z8aWpFRjB1MxACl3yvIbtvGITT1V1yw7B7ENXtOZZZLYP1Y=', 'HTTPStatusCode': 200, 'HTTPHeaders': {'x-amz-id-2': 'w1o+46zTKSTJ9bdekbzU2a6zfQd2z8aWpFRjB1MxACl3yvIbtvGITT1V1yw7B7ENXtOZZZLYP1Y=', 'x-amz-request-id': '8QN5K10WMX2ZG2ZS', 'date': 'Thu, 06 May 2021 15:48:54 GMT', 'last-modified': 'Fri, 15 Feb 2019 13:03:01 GMT', 'etag': '"24117d22703102e394fceb1a200de200"', 'content-encoding': 'gzip', 'accept-ranges': 'bytes', 'content-type': 'application/json', 'content-length': '252', 'server': 'AmazonS3'}, 'RetryAttempts': 0}, 'AcceptRanges': 'bytes', 'LastModified': datetime.datetime(2019, 2, 15, 13, 3, 1, tzinfo=tzutc()), 'ContentLength': 252, 'ETag': '"24117d22703102e394fceb1a200de200"', 'ContentEncoding': 'gzip', 'ContentType': 'application/json', 'Metadata': {}, 'Body': <botocore.response.StreamingBody object at 0x111f27f70>}
    @sanic.get("/schema/<id>")
    async def get_schema(request, id):
        get_object = s3.get_object(Bucket="funnel-data-schema-stage", Key=id + ".json")
        body = get_object['Body'].read()
        return raw(body, content_type="application/json", headers={"content-encoding": "gzip"})

    @sanic.post("/schema/<id>")
    async def write_schema(request, id):
        stream = io.StringIO(request.body.decode('utf-8'))
        s3.upload_fileobj(stream, Bucket="funnel-data-schema-stage", Key=id + ".json")
        return empty(status=201)

    return sanic


if __name__ == "__main__":
    server(boto3.client("s3")).run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
