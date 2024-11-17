import os
from typing import Awaitable, Dict, Any
from langchain_chroma import Chroma
from agnt_smth.core.utls import log, ChromaHttpClientFactory
from .embed import embed_file_system, create_embedding_function


embedding_function = create_embedding_function()
chroma_client = ChromaHttpClientFactory().create_with_auth()


async def process_embed_cmd(cmd: Dict[str, Any]) -> Awaitable:
    log(f"{process_embed_cmd.__name__} START.")

    file_system_path = cmd["file_system_path"]
    if not os.path.isdir(file_system_path):
        log(f"{process_embed_cmd.__name__} NOT A VALID DIR -> file_system_path: {file_system_path}")

    await embed_file_system(file_system_path)

    log(f"{process_embed_cmd.__name__} END.")


def create_retriever(collection_name: str):
    vector_store = Chroma(
        embedding_function=embedding_function,
        collection_name=collection_name,
        client=chroma_client,
    )
    retriever = vector_store.as_retriever()
    return retriever


async def process_qry_cmd(cmd: Dict[str, Any]) -> Awaitable:
    log(f"{process_qry_cmd.__name__} START.")

    collection_name = cmd["collection_name"]
    qry = cmd["qry"]

    retriever = create_retriever(collection_name)
    resp = retriever.invoke(qry)

    log(f"{process_qry_cmd.__name__} END.")

    return resp
