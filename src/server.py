import os

from sanic import Sanic, json


def server():
    sanic = Sanic("api")


    @sanic.get("/healthcheck")
    async def healthcheck(request):
        return json({"status": "ok"})

    return sanic

if __name__ == "__main__":
    server().run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
