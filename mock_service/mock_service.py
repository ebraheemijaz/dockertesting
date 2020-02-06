import asyncio
import os
import uuid
import logging

import httpx
from starlette.applications import Starlette
from starlette.background import BackgroundTask
from starlette.responses import JSONResponse
import uvicorn

app = Starlette()
client = httpx.AsyncClient()
CALLBACK_URL = "http://127.0.0.1:5000"

@app.route("/api/endpoint", methods=["POST"])
async def fake_endpoint(request):
    identifier = str(uuid.uuid4())
    payload = {
        "identifier": identifier,
        "some_parameter": request.query_params.get("some_parameter"),
    }
    task = BackgroundTask(trigger_webhook, payload)
    return JSONResponse(
        {"identifier": identifier, "success": True}, background=task)


async def trigger_webhook(payload):
    await asyncio.sleep(5)
    params = {
        "success": True,
        "identifier": payload["identifier"],
        "some_parameter": payload["some_parameter"],
    }
    await client.get(CALLBACK_URL, params=params)

@app.route("/api/endpoint/auth", methods=["POST"])
async def auth_endpoint(request):
    identifier = str(uuid.uuid4())
    payload = {
        "identifier": identifier,
        "username": request.query_params.get("username"),
        "password": request.query_params.get("password"),
    }
    task = BackgroundTask(trigger_webhook_auth, payload)
    return JSONResponse(
        {"identifier": identifier, "success": True}, background=task)

async def trigger_webhook_auth(payload):
    await asyncio.sleep(5)
    data = {
        "username": payload["username"],
        "password": payload["password"],
    }
    response = await client.post(CALLBACK_URL, data=data)
    logging.info(f'ReturnedData : {response.text}')


if __name__ == "__main__":
    host="0.0.0.0"
    port=8000
    uvicorn.run(app, host=host, port=port)