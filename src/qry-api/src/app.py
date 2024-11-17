import logging
from typing import Any, Dict
from json import dumps as json_dumps

from fastapi import FastAPI, Response, status
from fastapi.middleware.cors import CORSMiddleware

from dapr.ext.fastapi import DaprApp

from core import process_qry_cmd
from endpoints import healthz


logging.basicConfig(level=logging.DEBUG)


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(healthz.router)


@app.post("/qry")
async def handle_qry_cmd(cmd: Dict[str, Any]):
    logging.info(f"{handle_qry_cmd.__name__} START.")
    output = await process_qry_cmd(cmd)
    logging.info(f"{handle_qry_cmd.__name__} END.")
    resp = json_dumps({"output": output})
    return Response(content=resp, status_code=status.HTTP_200_OK)
