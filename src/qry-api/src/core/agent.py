import pprint
import functools
import operator
from typing import TypedDict, Sequence, Annotated

from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.graph import START, END, StateGraph
from langgraph.prebuilt.tool_executor import ToolExecutor

from agnt_smth.core.utls import log, ModelFactory, ChromaHttpClientFactory, EmbeddingFactory, RetrieverFactory
from agnt_smth.core.tools import RetrieveAdditionalContextTool
from agnt_smth.core.workflows import build_agnt_with_tools_graph

from .retrievers import RemoteEmbeddingRetriever

SYS_PROMPT = """
    You are a helpful agent with expertise in answering technical questions about a code repository.

    You should follow these guidelines:
    - Understand the Requirements: use the context retriever tool to look up the necessary information about the repository. You can use the context retriever tool as many times as you need to gather the necessary information.
    - Focus on Clarity and Accuracy: Ensure that the answer is clear, concise, and easy to understand, and accurate.
    - Formulate a Response: Format a response that addresses the question and provides the necessary information.
"""


def build_graph(repo_name: str):
    retriever = RemoteEmbeddingRetriever(api_url="http://localhost:6002")
    context_retriever = RetrieveAdditionalContextTool(retriever)
    tools = [context_retriever]

    return build_agnt_with_tools_graph(sys_prompt=SYS_PROMPT, tools=tools)
