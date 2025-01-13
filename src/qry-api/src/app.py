import logging
from typing import Any, Dict
from json import dumps as json_dumps

from fastapi import FastAPI, Response, status
from fastapi.middleware.cors import CORSMiddleware

from dapr.ext.fastapi import DaprApp

from core import process_qry_cmd, build_graph
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


WI_SYS_PROMPT = """
    You are a helpful agent with expertise in translating work item data in a rough text form to a structured formalized yaml structure.

    You should follow these guidelines:
    - Understand the Requirements: use the context retriever tool to look up the necessary information about the repository. You can use the context retriever tool as many times as you need to gather the necessary information.
    - Focus on Clarity and Accuracy: Ensure that the answer is clear, concise, and easy to understand, and accurate.
    - Formulate a Response: Format a response that addresses the question and provides the necessary information.
"""


GRAPHS = {}


@app.post("/build")
async def handle_build_cmd(cmd: Dict[str, Any]):
    logging.info(f"{handle_build_cmd.__name__} START.")

    graph = build_graph(cmd["file_system_path"], sys_prompt=WI_SYS_PROMPT)

    GRAPHS[cmd["file_system_path"]] = graph

    logging.info(f"{handle_build_cmd.__name__} END.")
    return Response(status_code=status.HTTP_200_OK)


@app.post("/qry")
async def handle_qry_cmd(cmd: Dict[str, Any]):
    logging.info(f"{handle_qry_cmd.__name__} START.")

    graph = GRAPHS.get(cmd["file_system_path"], None)

    output = await process_qry_cmd(cmd, graph)
    resp = json_dumps({"output": output})

    logging.info(f"{handle_qry_cmd.__name__} END.")
    return Response(content=resp, status_code=status.HTTP_200_OK)

