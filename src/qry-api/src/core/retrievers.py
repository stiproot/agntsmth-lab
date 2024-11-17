from langchain.schema import BaseRetriever, Document
import requests


class RemoteEmbeddingRetriever(BaseRetriever):
    def __init__(self, api_url: str):
        """
        Initializes the retriever.
        
        :param api_url: Base URL of the embeddings-api.
        """
        self.api_url = api_url

    def get_relevant_documents(self, query: str) -> list[Document]:
        """
        Retrieves relevant documents for a query.
        
        :param query: The input query.
        :return: A list of relevant LangChain Document objects.
        """
        response = requests.post(f"{self.api_url}/query", json={"query": query})
        response.raise_for_status()  # Ensure no HTTP errors
        results = response.json()  # Expecting results in a specific format
        
        # Convert API response to LangChain Documents
        documents = [
            Document(page_content=doc["text"], metadata=doc.get("metadata", {}))
            for doc in results.get("documents", [])
        ]
        return documents

    async def aget_relevant_documents(self, query: str) -> list[Document]:
        """
        Asynchronous retrieval of relevant documents.
        
        :param query: The input query.
        :return: A list of relevant LangChain Document objects.
        """
        import aiohttp
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self.api_url}/query", json={"query": query}) as response:
                if response.status != 200:
                    raise ValueError(f"Error from embeddings-api: {response.status}")
                results = await response.json()
                documents = [
                    Document(page_content=doc["text"], metadata=doc.get("metadata", {}))
                    for doc in results.get("documents", [])
                ]
                return documents
