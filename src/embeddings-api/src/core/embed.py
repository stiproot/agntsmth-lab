import os
from typing import List, Dict, Any, Awaitable
from langchain_chroma import Chroma
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from agnt_smth.core.utls import EnvVarProvider, log, traverse_folder, ChromaHttpClientFactory, generate_sha256
from .actors import create_embedding_actor_proxy


DEFAULT_CHUNK_SIZE = 1500
DEFAULT_CHUNK_OVERLAP = 50
DEFAULT_IGNORE_FOLDERS = ["node_modules", ".git", "bin", "obj", "__pycache__"]
DEFAULT_IGNORE_EXTENSIONS = [
    ".pfx",
    ".crt",
    ".cer",
    ".pem",
    ".postman_collection.json",
    ".postman_environment",
    ".png",
    ".gif",
    ".jpeg",
    ".jpg",
    ".ico",
    ".svg",
    ".woff",
    ".woff2",
    ".ttf",
    ".gz",
    ".zip",
    ".tar",
    ".tgz",
    ".tar.gz",
    ".rar",
    ".7z",
    ".pdf",
    ".doc",
    ".docx",
    ".xls",
    ".xlsx",
    ".ppt",
    ".pptx"
]

env = EnvVarProvider()


def translate_file_path_to_key(file_path: str) -> str:
    return file_path.replace(".", "__")


async def embed_file_system(file_system_path: str) -> Awaitable:
    log(f"{embed_file_system.__name__} START.")

    ####################################

    file_dict = traverse_folder(repo_target_dir, DEFAULT_IGNORE_FOLDERS, DEFAULT_IGNORE_EXTENSIONS)
    file_paths = [f"{k}/{f}" for k, v in file_dict.items() for f in v]
    actor = create_embedding_actor_proxy(repo_name)
    actor_state = await actor.get_state()

    log(f"{embed_file_system.__name__} -> file_paths: {file_paths}")

    ####################################

    chunk_size = env.get_env_var("CHUNK_SIZE", DEFAULT_CHUNK_SIZE)
    chunk_overlap = env.get_env_var("CHUNK_OVERLAP", DEFAULT_CHUNK_OVERLAP)
    chunk_hash = {}

    chroma_client = ChromaHttpClientFactory.create_with_auth()

    # todo: add support for other embedding functions
    # embedding_function = 

    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )
    vector_store = Chroma(
        embedding_function=embedding_function,
        client=chroma_client,
        collection_name=repo_name,
    )

    for file_path in file_paths:

        loader = TextLoader(file_path)
        docs = loader.load()

        page_content = docs[0].page_content
        hash = generate_sha256(page_content)

        if file_path in actor_state:
            if actor_state.get("file_path", {}).get("hash", None):
                log(f"{embed_file_system.__name__} SKIPPING -> {file_path} already embedded.")
                continue

        split_docs = text_splitter.split_documents(docs)
        split_texts = [doc.page_content for doc in split_docs]

        if not len(split_texts):
            continue

        embeddings = embedding_function.embed_documents(split_texts)
        ids = [f"{file_path}_{i}" for i in range(len(embeddings))]

        vector_store.add_documents(documents=split_docs, embeddings=embeddings, ids=ids)

        key = translate_file_path_to_key(file_path)

        if not actor_state.get("file_path", None):
            actor_state[key] = {}

        actor_state[key]["hash"] = hash
        await actor.set_state(actor_state)

    ####################################

    log(f"{embed_file_system.__name__} END.")
