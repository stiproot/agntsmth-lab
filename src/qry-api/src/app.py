import logging
from typing import Any, Dict
from json import dumps as json_dumps

from fastapi import FastAPI, Response, status
from fastapi.middleware.cors import CORSMiddleware

from dapr.ext.fastapi import DaprApp
from dapr.ext.fastapi import DaprActor
from dapr.actor.runtime.config import (
    ActorRuntimeConfig,
    ActorTypeConfig,
    ActorReentrancyConfig,
)
from dapr.actor.runtime.runtime import ActorRuntime

from core import process_qry_cmd, process_build_agnt_cmd, AgntActor
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

actor_runtime_config = ActorRuntimeConfig()
actor_runtime_config.update_actor_type_configs(
    [
        ActorTypeConfig(
            actor_type=AgntActor.__name__,
            reentrancy=ActorReentrancyConfig(enabled=True),
        )
    ]
)
ActorRuntime.set_actor_config(actor_runtime_config)

dapr_actor = DaprActor(app)


@app.on_event("startup")
async def startup_event():
    logging.info("Registering actors...")
    await dapr_actor.register_actor(AgntActor)


@app.post("/build-agnt")
async def handle_build_agnt_cmd(cmd: Dict[str, Any]):
    logging.info(f"{handle_build_agnt_cmd.__name__} START.")

    await process_build_agnt_cmd(cmd)

    logging.info(f"{handle_build_agnt_cmd.__name__} END.")
    return Response(status_code=status.HTTP_200_OK)


@app.post("/qry")
async def handle_qry_cmd(cmd: Dict[str, Any]):
    logging.info(f"{handle_qry_cmd.__name__} START.")

    output = await process_qry_cmd(cmd)
    resp = json_dumps({"output": output})

    logging.info(f"{handle_qry_cmd.__name__} END.")
    return Response(content=resp, status_code=status.HTTP_200_OK)

