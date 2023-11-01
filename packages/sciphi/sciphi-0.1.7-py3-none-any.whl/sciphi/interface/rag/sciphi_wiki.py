import os
from dataclasses import dataclass
from textwrap import dedent

import requests

from sciphi.core import RAGProviderName
from sciphi.interface.base import RAGInterface, RAGProviderConfig
from sciphi.interface.rag_interface_manager import rag_config, rag_provider


@dataclass
@rag_config
class SciPhiWikiRAGConfig(RAGProviderConfig):
    """An abstract class to hold the configuration for a RAG provider."""

    provider_name: RAGProviderName = RAGProviderName.SCIPHI_WIKI
    api_base: str = "https://api.sciphi.ai"
    top_k: int = 10


@rag_provider
class SciPhiWikiRAGInterface(RAGInterface):
    """A RAG provider that uses Wikipedia as the retrieval source."""

    provider_name = RAGProviderName.SCIPHI_WIKI
    FORMAT_INDENT = "        "

    def __init__(
        self,
        config: SciPhiWikiRAGConfig = SciPhiWikiRAGConfig(),
        *args,
        **kwargs,
    ) -> None:
        super().__init__(config)
        self.config: SciPhiWikiRAGConfig = config

    def get_contexts(self, prompts: list[str]) -> list[str]:
        """Get the context for a prompt."""
        api_key = self.config.api_key or os.getenv("SCIPHI_API_KEY")
        if not api_key:
            raise ValueError(
                "No API key provided. Please provide an API key or set the SCIPHI_API_KEY environment variable."
            )
        raw_contexts = wiki_search_api(
            prompts,
            self.config.api_base,
            api_key,
            self.config.top_k,
        )

        return [
            self._format_wiki_context(raw_context)
            for raw_context in raw_contexts
        ]

    def _format_wiki_context(self, context: dict) -> str:
        """Format the context for a prompt."""
        joined_context = [f"{ele['title']}\n{ele['text']}" for ele in context]
        return "\n".join(
            f"{SciPhiWikiRAGInterface.FORMAT_INDENT}{dedent(entry)}"
            for entry in joined_context
        )[: self.config.max_context]


def wiki_search_api(
    queries: list[str],
    rag_api_base: str,
    rag_api_key: str,
    top_k=10,
    batch_size=64,
) -> list[dict]:
    """
    Queries the search API with the provided credentials and query.
    The expected output is a JSON response containing the top_k examples.
    """

    def _send_request(batch_queries: list[str]) -> dict:
        """Helper function to send the request."""
        response = requests.post(
            f"{rag_api_base}/search",
            json={"queries": batch_queries, "top_k": top_k},
            headers={"Authorization": f"Bearer {rag_api_key}"},
        )
        if response.status_code != 200:
            if "detail" in response.json():
                raise ValueError(
                    f'Unexpected response from API - {response.json()["detail"]}'
                )
            else:
                raise ValueError(
                    f"Unexpected response from API - {response.json()}"
                )
        return response.json()

    # Break the list of queries into chunks of 'batch_size'
    results: list[dict] = []
    for i in range(0, len(queries), batch_size):
        batch = queries[i : i + batch_size]
        results.extend(_send_request(batch))

    return results
