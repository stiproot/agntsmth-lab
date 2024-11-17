import logging
from typing import Any, Dict

from fastapi import FastAPI, Response, status
from fastapi.middleware.cors import CORSMiddleware
from dapr.ext.fastapi import DaprApp

from core import process_embed_cmd
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


@app.post("/embed")
async def handle_embed_cmd(cmd: Dict[str, Any]):
    logging.info(f"{handle_embed_cmd.__name__} START.")
    await process_embed_cmd(cmd)
    logging.info(f"{handle_embed_cmd.__name__} END.")
