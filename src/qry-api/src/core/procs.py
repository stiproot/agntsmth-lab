from typing import Awaitable, Dict, Any, Optional
from langchain_core.messages import HumanMessage
from agnt_smth.core.utls import log
from .agent import build_graph


async def process_qry_cmd(cmd: Dict[str, Any], graph: Optional[any] = None) -> Awaitable:
    log(f"{process_qry_cmd.__name__} START.")

    qry = cmd["qry"]
    file_system_path = cmd["file_system_path"]

    log(f"{process_qry_cmd.__name__} -> qry: {qry}")

    graph = graph if graph is not None else build_graph(file_system_path)

    input = {"messages": [HumanMessage(content=qry)]}
    output = graph.invoke(input=input)

    log(f"{process_qry_cmd.__name__} -> output: {output}")
    log(f"{process_qry_cmd.__name__} END.")

    return output["messages"][-1].content
