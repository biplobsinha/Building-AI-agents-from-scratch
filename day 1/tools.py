from pathlib import Path

from ddgs.exceptions import DDGSException
from langchain_community.tools import DuckDuckGoSearchRun, WikipediaQueryRun
from langchain_community.utilities import (
    DuckDuckGoSearchAPIWrapper,
    WikipediaAPIWrapper,
)
from langchain_core.tools import tool

_search = DuckDuckGoSearchRun(
    api_wrapper=DuckDuckGoSearchAPIWrapper(backend="duckduckgo")
)
_wikipedia = WikipediaQueryRun(
    api_wrapper=WikipediaAPIWrapper(top_k_results=3, doc_content_chars_max=4000)
)


@tool
def search_tool(query: str) -> str:
    """Search the web for current information about a topic."""
    try:
        return _search.run(query)
    except DDGSException as error:
        return (
            "Web search is currently unavailable. Try the Wikipedia tool or "
            f"tell the user that web search failed. Details: {error}"
        )


@tool
def wiki_tool(query: str) -> str:
    """Search Wikipedia for background information about a topic."""
    return _wikipedia.run(query)


@tool
def save_tool(content: str) -> str:
    """Save research content to research_output.txt beside this script."""
    output_path = Path(__file__).with_name("research_output.txt")
    output_path.write_text(content, encoding="utf-8")
    return f"Saved research output to {output_path.name}."
