import os
from typing import Awaitable, Dict, Any
from agnt_smth.core.utls import log
from .embed import embed_file_system


async def process_embed_cmd(cmd: Dict[str, Any]) -> Awaitable:
    log(f"{process_embed_cmd.__name__} START.")

    file_system_path = cmd["file_system_path"]
    if not os.path.isdir(file_system_path):
        log(f"{process_embed_cmd.__name__} NOT A VALID DIR -> file_system_path: {file_system_path}")

    await embed_file_system(file_system_path)

    log(f"{process_embed_cmd.__name__} END.")
