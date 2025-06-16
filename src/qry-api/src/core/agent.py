import pprint
import functools
import operator
from typing import TypedDict, Sequence, Annotated

from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.graph import START, END, StateGraph
from langgraph.prebuilt.tool_executor import ToolExecutor

from agntsmth_core.core.utls import log, ModelFactory, ChromaHttpClientFactory, EmbeddingFactory, RetrieverFactory
from agntsmth_core.core.tools import RetrieveAdditionalContextTool
from agntsmth_core.core.workflows import build_agnt_with_tools_graph

from .retrievers import RemoteEmbeddingRetriever

DEFAULT_SYS_PROMPT = """
    You are a helpful agent with expertise in answering technical questions about a code repository.

    You should follow these guidelines:
    - Understand the Requirements: use the context retriever tool to look up the necessary information about the repository. You can use the context retriever tool as many times as you need to gather the necessary information.
    - Focus on Clarity and Accuracy: Ensure that the answer is clear, concise, and easy to understand, and accurate.
    - Formulate a Response: Format a response that addresses the question and provides the necessary information.
"""


def build_context_graph(sys_prompt: str, file_system_path: str) -> StateGraph:
    retriever = RemoteEmbeddingRetriever("http://localhost:6002", file_system_path)
    context_retriever = RetrieveAdditionalContextTool(retriever)
    tools = [context_retriever]

    return build_agnt_with_tools_graph(sys_prompt=sys_prompt, tools=tools)
