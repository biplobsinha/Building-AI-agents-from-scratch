# Research Assistant: A Beginner's Guide

Welcome! This README is a learning companion for the research assistant in this
folder. It explains what the program does, how to set it up, what the important
Python words and symbols mean, how the files fit together, and how to diagnose
common problems.

You do not need to understand everything before running the program. Try it,
read one section at a time, and change small pieces to see what happens.

## Table of contents

1. [What this project does](#what-this-project-does)
2. [Project files](#project-files)
3. [What happens when you run it](#what-happens-when-you-run-it)
4. [Before you start](#before-you-start)
5. [Set up the project](#set-up-the-project)
6. [Keep your API key private](#keep-your-api-key-private)
7. [Run the program](#run-the-program)
8. [Libraries and dependencies](#libraries-and-dependencies)
9. [A Python foundations primer](#a-python-foundations-primer)
10. [Line-by-line guide to `main.py`](#line-by-line-guide-to-mainpy)
11. [Line-by-line guide to `tools.py`](#line-by-line-guide-to-toolspy)
12. [Understanding the output](#understanding-the-output)
13. [Troubleshooting](#troubleshooting)
14. [Ideas for learning by changing the code](#ideas-for-learning-by-changing-the-code)
15. [Glossary](#glossary)

## What this project does

This is a small command-line research assistant. You type a question, and a
language model hosted by Groq can decide whether to use the tools provided to
it:

- **Web search:** looks for web results using the DuckDuckGo search integration.
- **Wikipedia:** looks up background information in Wikipedia.
- **Save:** writes text to a file named `research_output.txt` if the model
  chooses to call this tool.

After the agent finishes its research, the program asks the model to format the
result as JSON and validate it against a Pydantic model. The JSON has four
fields: `topic`, `summary`, `sources`, and `tools_used`.

The program needs internet access to call Groq and to use online research
services. In particular, web search may fail because of DNS, network, or service
availability. The search tool is written to report a DuckDuckGo search failure
to the agent so it can try another tool. Wikipedia errors are not currently
handled in the same way.

## Project files

```text
Building AI agents/
├── .venv/                 # Virtual environment at the workspace root
└── day 1/
    ├── .env               # Your private Groq API key; do not share this file
    ├── main.py            # Starts the agent and asks for your question
    ├── requirement.txt    # Python packages needed by this lesson
    ├── tools.py           # Search, Wikipedia, and save tools
    └── README.md          # This learning guide
```

The virtual environment shown above is one folder above `day 1`. A virtual
environment is a private Python installation for a project. It keeps this
project's installed packages separate from other Python projects on your
computer.

## What happens when you run it

Here is the program's journey from input to output:

1. Python loads the packages and functions used by `main.py`.
2. `python-dotenv` reads the `GROQ_API_KEY` value from `.env`.
3. The program creates a Groq chat model using the configured model name.
4. LangChain creates an agent and gives it the search, Wikipedia, and save
   tools.
5. The program asks you to type a question.
6. The agent sends the question to the model. The model may request one or more
   tools; LangChain runs those tools and gives the results back to the model.
7. The agent returns a final research message.
8. A separate model request formats that message as the four-field
   `ResearchResponse` JSON structure.
9. Python prints the formatted JSON to the terminal.

The second model request is separate on purpose. Groq's JSON response mode
cannot be combined with tool/function calling in the same request for this
model. The first request uses tools; the second request formats the result as
JSON without tools.

## Before you start

You will need:

- Python installed on your computer.
- The project virtual environment set up with the packages in
  `requirement.txt`.
- A Groq account and a Groq API key.
- Internet access for the Groq API and online research tools.
- A terminal. The examples below use **PowerShell**, which is the terminal
  shown in this project's recent runs.

The instructions assume this project folder:

```text
C:\Users\Biplob\Desktop\Building AI agents
```

If you moved the folder, use your own folder path instead.

## Set up the project

### 1. Open a terminal at the workspace root

In VS Code, choose **Terminal → New Terminal**. The workspace root is the
`Building AI agents` folder, one level above `day 1`.

### 2. Activate the existing virtual environment (PowerShell)

If your prompt already begins with `(.venv)`, it is active and you can skip
this step. Otherwise, from the workspace root run:

```powershell
.\.venv\Scripts\Activate.ps1
```

The `.\` means “start from the current folder.” `Scripts\Activate.ps1` is the
PowerShell activation script inside the virtual environment.

If PowerShell blocks the activation script, you can avoid activation and call
the virtual environment's Python directly:

```powershell
& ".\.venv\Scripts\python.exe" ".\day 1\main.py"
```

PowerShell uses `&` (the call operator) to run a quoted executable path.

### 3. Install or refresh the dependencies

Run this from the workspace root:

```powershell
python -m pip install -r ".\day 1\requirement.txt"
```

If the virtual environment is not activated, use its Python explicitly:

```powershell
& ".\.venv\Scripts\python.exe" -m pip install -r ".\day 1\requirement.txt"
```

What each part means:

- `python` runs Python. When the virtual environment is active, this should be
  the virtual environment's Python.
- `-m pip` tells Python to run the `pip` package installer module.
- `install` asks pip to install packages.
- `-r` means “read the package names from a requirements file.”
- The quoted path points to this lesson's `requirement.txt`. Quotes are
  important because `Building AI agents` contains spaces.

## Keep your API key private

The `.env` file stores your API key so you do not have to put the key in the
Python source code. Its contents should look like this:

```dotenv
GROQ_API_KEY=put_your_new_groq_key_here
```

Replace `put_your_new_groq_key_here` with your own key. Do not include the
placeholder text literally. Do not paste the real key into chat, screenshots,
source files, or a public repository.

An API key is a secret credential: it allows software to make requests as your
account. If you have exposed a key, revoke or rotate it in your Groq account and
put the replacement in `.env`.

The `.env` file is normally excluded from version control. If you use Git,
check that it is ignored before sharing or publishing the project. Never put a
real API key into this README.

## Run the program

From the workspace root, with `(.venv)` active:

```powershell
python ".\day 1\main.py"
```

Then type a question at the prompt, for example:

```text
What can I help you research? Paolo Maldini
```

Press **Enter** to submit it. The program prints a JSON object when it finishes.

You can also change into the lesson folder first:

```powershell
cd ".\day 1"
python .\main.py
```

`cd` means “change directory.” The quotes around `.\day 1` are needed because
the directory name contains a space.

## Libraries and dependencies

A **library** is reusable code written by other people that your program can
import. A **package** is an installable distribution of code. The names in
`requirement.txt` are package names; Python import names sometimes differ from
package names.

| Requirement | What it is for | Used directly by this lesson? |
|---|---|---|
| `langchain` | Framework for building applications that call language models and tools. This code imports `create_agent` from it. | Yes |
| `wikipedia` | Wikipedia-related Python integration dependency. | Indirectly through the LangChain Wikipedia integration |
| `langchain-community` | Community-maintained LangChain integrations, including DuckDuckGo and Wikipedia wrappers. | Yes, in `tools.py` |
| `langchain-openai` | LangChain integration for OpenAI-compatible services. | No; not imported by the current lesson |
| `langchain-anthropic` | LangChain integration for Anthropic's Claude models. | No; not imported by the current lesson |
| `langchain-groq` | LangChain integration for Groq chat models. | Yes, in `main.py` |
| `python-dotenv` | Reads key-value settings from a `.env` file into environment variables. | Yes, in `main.py` |
| `pydantic` | Defines and validates data using Python classes and type annotations. | Yes, in `main.py` |
| `ddgs` | Provides the DuckDuckGo search implementation used by the community integration. | Yes, indirectly through the search wrapper |

The requirements file may include packages used by other lessons or planned
experiments. An entry in the file does not necessarily mean this particular
script imports it. For example, the current `main.py` uses Groq, not the
OpenAI or Anthropic LangChain integrations.

### Package name versus import name

`requirement.txt` contains `langchain-groq`, but the Python import is
`langchain_groq`. Package installers conventionally use hyphens in some package
names; Python import statements use valid Python identifiers, so the import
uses an underscore instead.

Similarly, the package is named `python-dotenv`, while the imported module is
named `dotenv`.

## A Python foundations primer

These are the main Python ideas used in this project:

- **Statement:** An instruction Python executes, such as `load_dotenv()`.
- **Name / variable:** A label referring to a value, such as `query` or `llm`.
- **String:** Text surrounded by quotes, such as `"GROQ_API_KEY"`.
- **Function:** Reusable instructions. A function is defined with `def` and
  called with parentheses, as in `search_tool(query)`.
- **Argument:** A value passed into a function, such as the prompt string in
  `input("What can I help you research? ")` or `query` in `_search.run(query)`.
- **Return value:** The result a function gives back. `input(...)` returns the
  text you type.
- **Class:** A blueprint for creating objects. `ResearchResponse` is a class.
- **Object / instance:** A value created from a class. A `ChatGroq(...)`
  expression creates a model object.
- **Attribute:** A value or function accessed after a dot, such as
  `response.content`.
- **Module:** A Python file or importable library. `os` and `sys` are standard
  library modules.
- **Import:** A statement that makes a name from a module available in this
  file.
- **Type annotation:** A hint about the kind of value expected, such as
  `query: str` or `sources: list[str]`. It improves clarity and can be checked
  by tools; it does not by itself convert a value.
- **Decorator:** A function-like marker written with `@` above a definition.
  `@tool` turns a regular Python function into a LangChain tool.
- **Exception:** An object representing an error. `try` and `except` can handle
  selected exceptions.
- **Environment variable:** A named setting available to a running process.
  `GROQ_API_KEY` is read this way so the secret is not hard-coded in Python.
- **JSON:** A text format for structured data, using objects, arrays, strings,
  numbers, booleans, and `null`. JSON is commonly used by web APIs.

### Punctuation you will see

- `()` calls a function or groups parameters.
- `,` separates arguments or items.
- `.` accesses a module member or object attribute.
- `=` assigns a value to a name, or separates a named argument from its value.
- `:` begins an indented block or separates a name from its type annotation.
- `""` or `''` marks a string.
- `""` repeated three times can mark a docstring that spans lines.
- `[]` creates a list or selects an item, such as the final message with
  `messages[-1]`.
- `{}` creates a dictionary, a collection of key-value pairs.
- `@` applies a decorator.
- `_` is allowed in Python names. A leading underscore conventionally means
  “internal implementation detail”; Python does not make the name truly
  private.
- `f"..."` is an f-string. Expressions inside `{...}` are evaluated and added
  to the text.

Indentation (spaces at the beginning of a line) is meaningful in Python. Lines
inside a class, function, or `try` block are indented to show which block they
belong to. Keep indentation consistent; four spaces per level is the common
style.

## Line-by-line guide to `main.py`

The snippets below correspond to the current source file. Line numbers are
not printed beside each line here, so use the section headings or search for a
distinctive line in your editor to find each section.

### Imports and startup

```python
import os
import sys

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_groq import ChatGroq
from pydantic import BaseModel

from tools import save_tool, search_tool, wiki_tool

load_dotenv()
sys.stdout.reconfigure(encoding="utf-8")
```

- `import os` loads Python's built-in operating-system utilities. This program
  uses `os.getenv(...)` to read an environment variable.
- `import sys` loads Python's built-in interpreter and system utilities. This
  program uses `sys.stdout` to configure terminal output.
- The blank lines only separate groups to make the file easier to read.
- `from dotenv import load_dotenv` imports just the `load_dotenv` function from
  the third-party `dotenv` module.
- `from langchain.agents import create_agent` imports LangChain's agent
  constructor. An agent is a model-based program that can decide to call tools.
- `from langchain_groq import ChatGroq` imports the LangChain class that
  connects a chat model to Groq.
- `from pydantic import BaseModel` imports Pydantic's base class. The response
  schema below inherits from it.
- `from tools import save_tool, search_tool, wiki_tool` imports the three tool
  functions defined in this folder's `tools.py`. Python finds `tools.py`
  because it is beside `main.py`.
- `load_dotenv()` reads `.env` and makes its entries available through
  `os.getenv`. With no path given, `python-dotenv` searches for a `.env` file.
- `sys.stdout` is the stream where `print(...)` writes. `reconfigure` sets its
  text encoding to UTF-8 so characters such as curly quotes are less likely to
  cause errors in Windows terminals.

### The response data shape

```python
class ResearchResponse(BaseModel):
    topic: str
    summary: str
    sources: list[str]
    tools_used: list[str]
```

- `class` begins a class definition.
- `ResearchResponse` is the class name. By convention, Python class names use
  `CapWords` capitalization.
- `(BaseModel)` means `ResearchResponse` inherits behavior from Pydantic's
  `BaseModel`.
- The indented lines declare the data fields that a response must contain.
- `topic: str` says `topic` should be text. `str` is Python's string type.
- `summary: str` says `summary` should also be text.
- `sources: list[str]` says `sources` should be a list whose items are strings.
  `list` is Python's ordered, changeable collection type.
- `tools_used: list[str]` describes a list of tool names, also as strings.
- Pydantic validates values against these annotations when it creates a
  `ResearchResponse`. A missing required field or a wrong type can produce a
  validation error.

This is a **schema**: a description of the shape data should have. It is not the
research itself.

### Find and configure the API key

```python
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("GROQ_API_KEY is missing. Add it to the .env file.")
```

- `os.getenv("GROQ_API_KEY")` asks the operating system for the value named
  `GROQ_API_KEY`. The quotes contain the variable's name, not the key itself.
- `api_key = ...` stores the result in a variable named `api_key`.
- `if` begins a conditional: the indented code runs only if its condition is
  true.
- `not api_key` is true if the value is missing or empty.
- `raise` deliberately stops the program by raising an error.
- `ValueError` is a built-in Python error type used here to explain the
  configuration problem clearly.
- The message tells you which setting is missing. It does not reveal the
  secret.

This check is called **input/configuration validation**. It catches a missing
key before the program makes a network request.

```python
llm = ChatGroq(
    model="openai/gpt-oss-120b",
    api_key=api_key,
    temperature=0,
)
```

- `llm` is a variable name, commonly short for “large language model.”
- `ChatGroq(...)` creates a LangChain chat-model object configured for Groq.
- `model=...` is a named argument. It selects the model identifier sent to
  Groq. The model must remain available to your Groq account; providers can
  change their model catalogue.
- `api_key=api_key` passes the value read from `.env`. The first `api_key` is
  the parameter name; the second is the Python variable.
- `temperature=0` asks for lower-randomness output. It does not guarantee
  perfectly identical answers.
- The trailing comma after the last argument is allowed and makes later edits
  easier.

### Create the agent

```python
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
```

- `create_agent(...)` builds a LangChain agent for the installed LangChain
  version.
- `model=llm` gives the agent the Groq chat model it should ask for decisions
  and responses.
- `tools=[...]` gives the agent a Python list of functions it may call. The
  square brackets create the list; commas separate its items.
- The agent can choose tools; merely placing a tool in the list does not mean
  it runs on every query.
- `system_prompt` is the instruction text that describes the assistant's role
  and behavior.
- Parentheses around the adjacent quoted strings allow the prompt to be split
  across multiple source lines. Python joins adjacent string literals into one
  string.
- The prompt requests research, sources, and tool names. It also tells the
  model not to claim an unavailable tool succeeded.
- The closing `)` ends the `create_agent(...)` call.

### Ask the question and run the agent

```python
query = input("What can I help you research? ")
result = agent.invoke({"messages": [{"role": "user", "content": query}]})
research_text = result["messages"][-1].content
```

- `input(...)` displays the prompt and waits for you to type. It returns the
  entered text as a string.
- `query = ...` saves the user's question.
- `agent.invoke(...)` runs the agent synchronously: Python waits for the
  request and tool work to finish before moving to the next line.
- The argument is a **dictionary**. A dictionary stores values under keys.
- The outer dictionary has a key named `"messages"`.
- Its value is a list containing a message dictionary.
- `"role": "user"` labels the message as coming from the user.
- `"content": query` sets the message text to the question you typed.
- `result` stores the agent's returned state, including its messages.
- `result["messages"]` retrieves the messages list by its key.
- `[-1]` selects the last item in the list. In Python, index `-1` means the
  final item.
- `.content` accesses the content attribute of that final message.
- `research_text` stores the agent's final text for the formatting step.

### Format the result as structured JSON

```python
structured_llm = llm.with_structured_output(
    ResearchResponse,
    method="json_mode",
)
```

- `llm.with_structured_output(...)` creates a version of the model configured
  to return data matching a schema.
- `ResearchResponse` is the schema class defined earlier.
- `method="json_mode"` asks Groq for JSON output mode. This formatting request
  has no tools attached, which avoids combining JSON mode with tool calling.
- The returned runnable is stored in `structured_llm`.

```python
structured_response: ResearchResponse = structured_llm.invoke(
    "Return valid JSON with exactly these fields: topic (string), summary "
    "(string), sources (array of strings), and tools_used (array of strings). "
    "Use only information present in the research, and do not invent sources.\n\n"
    f"User query: {query}\n\nResearch:\n{research_text}"
)
```

- `structured_response: ResearchResponse` is a variable assignment with a type
  annotation. It documents that the expected value is a `ResearchResponse`
  instance.
- `.invoke(...)` sends the formatting request to the model and waits for the
  answer.
- The first adjacent strings explain the exact required JSON fields. Giving
  explicit field names helps the model return the shape required by Pydantic.
- `\n` means “newline” inside a string. `\n\n` adds a blank line for
  readability.
- `f"..."` is an f-string. `{query}` and `{research_text}` are replaced by the
  values stored in those variables.
- The instruction says not to invent sources. Model output can still contain
  mistakes, so treat source claims as something to verify.
- The model's JSON is parsed and validated against `ResearchResponse`. The
  result is a Python object, not just an unvalidated text string.

```python
print(structured_response.model_dump_json(indent=2))
```

- `print(...)` writes text to the terminal.
- `.model_dump_json(...)` is a Pydantic method that serializes the model object
  into JSON text.
- `indent=2` formats the JSON using two spaces per indentation level, making
  it easier to read.

## Line-by-line guide to `tools.py`

### Imports and reusable integrations

```python
from pathlib import Path

from ddgs.exceptions import DDGSException
from langchain_community.tools import DuckDuckGoSearchRun, WikipediaQueryRun
from langchain_community.utilities import (
    DuckDuckGoSearchAPIWrapper,
    WikipediaAPIWrapper,
)
from langchain_core.tools import tool
```

- `Path` is a modern Python helper for working with file and folder paths.
- `DDGSException` is the error type raised by the DuckDuckGo search package.
  The code catches this specific kind of search failure.
- `DuckDuckGoSearchRun` is a LangChain tool wrapper that runs a search query.
- `WikipediaQueryRun` is a LangChain tool wrapper for a Wikipedia lookup.
- `DuckDuckGoSearchAPIWrapper` configures the underlying search integration.
- `WikipediaAPIWrapper` configures how many Wikipedia results and how much
  text to retrieve.
- Parentheses allow a long `from ... import ...` list to be split over several
  lines.
- `tool` is a decorator that adapts ordinary Python functions into LangChain
  tools with descriptions and input schemas.

### Configure the web-search and Wikipedia wrappers

```python
_search = DuckDuckGoSearchRun(
    api_wrapper=DuckDuckGoSearchAPIWrapper(backend="duckduckgo")
)
```

- `_search` stores the DuckDuckGo LangChain wrapper. The leading underscore is
  a convention meaning it is an internal helper for this module.
- `DuckDuckGoSearchAPIWrapper(backend="duckduckgo")` creates the lower-level
  search configuration and requests the DuckDuckGo backend instead of
  automatic backend selection.
- `api_wrapper=...` passes that configured wrapper into
  `DuckDuckGoSearchRun`.
- This configuration does not guarantee search will work: DNS, network access,
  and the search provider must still be available.

```python
_wikipedia = WikipediaQueryRun(
    api_wrapper=WikipediaAPIWrapper(top_k_results=3, doc_content_chars_max=4000)
)
```

- `_wikipedia` stores the Wikipedia tool wrapper.
- `WikipediaAPIWrapper(...)` configures the Wikipedia integration.
- `top_k_results=3` requests up to three matching results.
- `doc_content_chars_max=4000` limits the returned page text to about 4,000
  characters per result.
- These values control what the integration asks for; they do not guarantee
  that every query returns that many results.

### The web-search tool

```python
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
```

- `@tool` decorates the function immediately below it. LangChain reads the
  function name, type annotations, and docstring to describe the tool to the
  model.
- `def` starts a function definition.
- `search_tool` is the function name and tool name.
- `query: str` means the function expects a text query.
- `-> str` means the function is intended to return text.
- The colon `:` ends the function header and starts its indented body.
- The triple-quoted sentence is a **docstring**, a short description of the
  function. LangChain can show this description to the model.
- `try:` starts a block where a particular operation might fail.
- `_search.run(query)` sends the query to the configured search wrapper.
- `return` gives the wrapper's text back as the tool result and ends this
  function call.
- `except DDGSException as error:` catches only the specific DuckDuckGo
  exception named here and binds it to `error`.
- The fallback text tells the agent that search was unavailable; it does not
  pretend that search returned results.
- `f"...{error}"` inserts the exception's text into the fallback message.
- Other exception types are not caught by this `except` clause and may still
  stop the program. This is intentional rather than silently hiding every
  possible error.

### The Wikipedia tool

```python
@tool
def wiki_tool(query: str) -> str:
    """Search Wikipedia for background information about a topic."""
    return _wikipedia.run(query)
```

- `@tool` makes the function available to the agent.
- `wiki_tool` is the function/tool name.
- Its `query: str` input is a search phrase.
- `-> str` documents a text result.
- The docstring describes the purpose of the tool.
- `_wikipedia.run(query)` sends the query to the Wikipedia wrapper.
- `return` passes the wrapper's result back to the agent.
- Unlike `search_tool`, this function currently has no `try`/`except` handling.
  A network or Wikipedia API failure can therefore still stop the run.

### The save tool

```python
@tool
def save_tool(content: str) -> str:
    """Save research content to research_output.txt beside this script."""
    output_path = Path(__file__).with_name("research_output.txt")
    output_path.write_text(content, encoding="utf-8")
    return f"Saved research output to {output_path.name}."
```

- `@tool` makes this function available to the model-powered agent.
- `save_tool` is the tool name.
- `content: str` means it accepts the text that should be written.
- `Path(__file__)` creates a path object for this Python file. `__file__` is a
  special Python variable containing the current file's path.
- `.with_name("research_output.txt")` creates a sibling path with the new file
  name. “Sibling” means in the same folder as `tools.py`.
- `output_path` stores that destination.
- `.write_text(...)` writes text to the destination file.
- `encoding="utf-8"` selects UTF-8 text encoding.
- If the file already exists, `write_text` replaces its contents. It does not
  append.
- `output_path.name` gets only the final file name, not the entire path.
- The f-string returns a confirmation to the agent.

The agent may choose to use this tool, but the current `main.py` does not call
`save_tool` directly. If you want saving to happen every time, you would need to
change the program to call it explicitly or instruct the agent to use it.

## Understanding the output

A successful result looks like this shape:

```json
{
  "topic": "The subject you asked about",
  "summary": "A concise summary based on the agent's research",
  "sources": [
    "A source name or page used during research"
  ],
  "tools_used": [
    "wiki_tool"
  ]
}
```

This is an example of the **shape**, not a verified answer to any particular
question. Your actual values depend on the question, tool availability, and
model response.

- `{ ... }` is a JSON object.
- Each `"name": value` pair is a field.
- Strings are surrounded by double quotes.
- Arrays/lists are surrounded by square brackets.
- The source and tool fields can contain zero or more strings.

The Pydantic class validates the data's field names and types. It cannot prove
that a factual statement or citation is true. Always check important facts
against the cited sources.

## Troubleshooting

### `GROQ_API_KEY is missing`

Check that:

1. There is a file named `.env` inside `day 1`.
2. It contains a line like `GROQ_API_KEY=your_real_key`.
3. The key is active and was not revoked.
4. You are running the intended `main.py`.

Do not paste your key into the terminal command itself or into a public file.

### `python` runs a different interpreter or cannot find a package

Activate the project's virtual environment first:

```powershell
.\.venv\Scripts\Activate.ps1
```

Then install the requirements:

```powershell
python -m pip install -r ".\day 1\requirement.txt"
```

You can confirm which Python is active with:

```powershell
python --version
python -m pip --version
```

### Groq reports an unavailable or unknown model

The model name in `main.py` is `openai/gpt-oss-120b`. Check the models available
to your Groq account and update the `model=` value if Groq changes availability
or access. This setting is a provider model ID, not a local file.

### DuckDuckGo reports DNS errors or no results

Web search requires working DNS and network access to the search provider. A
DNS error means your computer could not resolve the provider's domain name to
an internet address. Check your internet connection, DNS settings, VPN, proxy,
or firewall and try again later.

The `search_tool` catches `DDGSException` and returns an unavailable message to
the agent. The agent may then try Wikipedia. It cannot make an unavailable
network connection work by itself.

### Wikipedia reports a network error

Wikipedia is also an online service. Check your connection and try again. The
current `wiki_tool` does not catch Wikipedia exceptions, so its error may
appear as a Python traceback.

### `UnicodeEncodeError` when printing

`main.py` configures standard output as UTF-8 with
`sys.stdout.reconfigure(encoding="utf-8")`. If you run the code in a custom
environment that does not support this method, check your Python version and
terminal configuration.

### The output has the wrong fields or fails validation

`ResearchResponse` requires `topic`, `summary`, `sources`, and `tools_used`.
The formatting prompt asks for exactly these names. If the model still returns
different fields, Pydantic may raise a validation error. Read the error to see
which field is missing or has the wrong type.

### Nothing was saved

The save tool only writes a file if the agent chooses to call it. If the agent
does call it, `research_output.txt` appears beside `tools.py`, in this `day 1`
folder. If you want a file on every run, explicitly call the tool from your
Python code rather than depending on the model to choose it.

## Ideas for learning by changing the code

Try one small change at a time, then run the program again:

1. Change the question prompt in `input(...)`.
2. Add a field to `ResearchResponse`, such as `key_points: list[str]`, and
   update the formatting instructions so the model fills it.
3. Change `top_k_results=3` in `tools.py` and observe how much Wikipedia text
   the tool returns.
4. Change the system prompt and compare how the agent behaves.
5. Ask the agent to use `save_tool` and see whether it creates
   `research_output.txt`.
6. Deliberately remove `GROQ_API_KEY` from `.env` and observe the clear
   configuration error; then restore it.
7. Add print statements to inspect values such as `query` and `research_text`.
   Do not print `api_key`.

When experimenting, keep a working copy or use version control so you can
recover from changes you do not want.

## Glossary

| Term | Plain-language meaning |
|---|---|
| Agent | A program that uses a model to decide what action to take, such as calling a tool. |
| API | A defined way for one program to request a service from another program. |
| API key | A secret credential used to authenticate requests to an API. |
| Argument | A value supplied to a function call. |
| Backend | The service or implementation that performs an operation such as a search. |
| Class | A blueprint that defines how a kind of object behaves and stores data. |
| Command line / terminal | A text interface where you run commands and programs. |
| Dependency | A package or library that a project needs in order to work. |
| Environment variable | A named setting supplied to a running process. |
| Exception | A Python object that represents an error or unusual condition. |
| Function | A reusable block of Python instructions. |
| JSON | A text representation for structured values, commonly used by APIs. |
| Language model | Software trained to process and generate language. |
| Method | A function associated with an object, called using dot notation. |
| Model | Here, the specific language model selected from the provider. |
| Package | Installable Python software, often containing one or more modules. |
| Pydantic | A Python library for defining and validating data structures. |
| Schema | A description of the names and types expected in structured data. |
| Tool | A function an agent is allowed to call to perform an operation. |
| Type | A category of value, such as text (`str`) or a list (`list`). |
| Virtual environment | An isolated Python installation for a project. |

Enjoy the journey. Learning to read code is a skill built one line, one
experiment, and one error message at a time.
