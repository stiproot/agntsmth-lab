from typing import Awaitable, Dict, Any, Optional
from langchain_core.messages import HumanMessage
from agntsmth_core.core.utls import log
from .agent import build_context_graph
from .actors import create_agnt_actor_proxy


GRAPHS = {}


async def process_build_agnt_cmd(cmd: Dict[str, Any], graph: Optional[any] = None) -> Awaitable:
    log(f"{process_build_agnt_cmd.__name__} START.")

    agnt_id = cmd["agnt_id"]
    sys_prompt = cmd["sys_prompt"]
    file_system_path = cmd.get("file_system_path", None)

    actor = create_agnt_actor_proxy(agnt_id)

    actor_state = await actor.get_state()
    actor_state["sys_prompt"] = sys_prompt
    actor_state["file_system_path"] = file_system_path

    await actor.set_state(actor_state)

    log(f"{process_build_agnt_cmd.__name__} END.")


async def process_qry_cmd(cmd: Dict[str, Any], graph: Optional[any] = None) -> Awaitable:
    log(f"{process_qry_cmd.__name__} START.")

    agnt_id = cmd["agnt_id"]
    qry = cmd["qry"]

    log(f"{process_qry_cmd.__name__} -> agnt_id: {agnt_id}, qry: {qry}")

    actor = create_agnt_actor_proxy(agnt_id)
    actor_state = await actor.get_state()

    file_system_path = actor_state["file_system_path"]
    sys_prompt = actor_state["sys_prompt"]

    if agnt_id not in GRAPHS:
        GRAPHS[agnt_id] = build_context_graph(sys_prompt, file_system_path)

    graph = GRAPHS[agnt_id]

    input = {"messages": [HumanMessage(content=qry)]}
    output = graph.invoke(input=input)

    log(f"{process_qry_cmd.__name__} -> output: {output}")
    log(f"{process_qry_cmd.__name__} END.")

    return output["messages"][-1].content
