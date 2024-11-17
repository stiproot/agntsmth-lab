from typing import Awaitable, Dict, Any
from langchain_core.messages import HumanMessage
from agnt_smth.core.utls import log
from .agent import build_graph


async def process_qry_cmd(cmd: Dict[str, Any]) -> Awaitable:
    log(f"{process_qry_cmd.__name__} START.")

    qry = cmd["qry"]

    log(f"{process_qry_cmd.__name__} -> qry: {qry}")

    graph = build_graph(repo_name)
    input = {"messages": [HumanMessage(content=qry)]}
    output = graph.invoke(input=input)

    log(f"{process_qry_cmd.__name__} -> output: {output}")
    log(f"{process_qry_cmd.__name__} END.")

    return output["messages"][-1].content
