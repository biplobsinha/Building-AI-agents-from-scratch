import os
import sys

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_groq import ChatGroq
from pydantic import BaseModel

from tools import save_tool, search_tool, wiki_tool

load_dotenv()
sys.stdout.reconfigure(encoding="utf-8")


class ResearchResponse(BaseModel):
    topic: str
    summary: str
    sources: list[str]
    tools_used: list[str]


api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("GROQ_API_KEY is missing. Add it to the .env file.")

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    api_key=api_key,
    temperature=0,
)

agent = create_agent(
    model=llm,
    tools=[search_tool, wiki_tool, save_tool],
    system_prompt=(
        "You are a research assistant. Research the user's query using the "
        "available tools when useful. Provide a concise summary, list the "
        "sources you used, and name the tools you used. If a tool reports an "
        "error or unavailable service, do not claim it succeeded; continue "
        "with other available sources and mention the limitation."
    ),
)

query = input("What can I help you research? ")
result = agent.invoke({"messages": [{"role": "user", "content": query}]})
research_text = result["messages"][-1].content
structured_llm = llm.with_structured_output(
    ResearchResponse,
    method="json_mode",
)
structured_response: ResearchResponse = structured_llm.invoke(
    "Return valid JSON with exactly these fields: topic (string), summary "
    "(string), sources (array of strings), and tools_used (array of strings). "
    "Use only information present in the research, and do not invent sources.\n\n"
    f"User query: {query}\n\nResearch:\n{research_text}"
)
print(structured_response.model_dump_json(indent=2))
