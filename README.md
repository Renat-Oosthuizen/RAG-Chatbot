# RAG-Chatbot (Proof of Concept)
This project demonstrates tool use in a LLM agent which will pick the most appropriate tool to use in the context provided by the user. This project utilises the LlamaIndex framework.
The agent has Retrieval Augmented Generation (RAG) capabilities allowing it to retrieve information from user provided sources in order to fulfill the user's request.
The LLM model used is OpenAI's `gpt-3.5-turbo-0613`, connected to via their API.
This agent has access to the following tools:
- Note Engine allowing the agent to write notes in a `notes.txt` file at the user's request.
- PandasQueryEngine allowing the agent to read CSV documents. For demonstration purposes it has been provided a `population.csv` file with population data.
- DocXReader allowing the agent to read Microsoft Word Documents specifically. For demonstration purposes it has been provided `UK.docsx` file containing the contents of the United Kingdom wikipedia page.
- SimpleDirectoryReader allowing the agent to read from common unstructured file formats including `.pdf`, `.txt`, `.md` and `docx`.

![Agent Answers 1.JPG](rag-chatbot%2FReadMe%20Images%2FAgent%20Answers%201.JPG)

![Agent Answers 2.JPG](rag-chatbot%2FReadMe%20Images%2FAgent%20Answers%202.JPG)

## Setup

- Create the file `RAG-Chatbot\rag-chatbot\.env`. This file should contain `OPENAI_API_KEY=[key]`. You need to set the value to your OpenAI API key which you can get from [OpenAI](https://platform.openai.com/api-keys). You may need to create an account first.
- Make sure that Poetry dependency manager is installed using `pip install poetry`.
- In the project root directory run: 
```bash
poetry install  # Installs all necessary dependencies defined in pyproject.toml
poetry shell  # Enter the poetry virtual environment that has the installed dependencies
make run  # Run the application using the command from the Makefile, equivalent to `python rag-chatbot/main.py`
```
Note: 
- If poetry install fails, you may need to run `pip install PyMuPDF`. PyMuPDF is a dependency of llama-index that poetry seems to struggle installing.
- If using Windows OS, you may need to install the `make` utility first, before you can run make commands. 
See [here](https://earthly.dev/blog/makefiles-on-windows/) and [here](https://chocolatey.org/install) for guidance on how to install the chocolatey package manager and then use it to install `make`.
Alternatively, simply run `python rag-chatbot/main.py` in terminal.


## Project Map

```bash
├───rag-chatbot               # Package containing the application.
│   ├───ReadMe Images         # Images that are only used for this ReadMe file.
│   ├───data                  # Directory containing population.csv and UK.docx to be used by the agent. When a note is written by the agent, notes.txt will be generated here.
│   ├───varied_data           # Directory contains various file types that will be read by the agent.
│   ├───definitions.py        # Contains ROOT_DIR variable that always holds path to the repository root directory. 
│   ├───doc_reader.py         # Tools used by the agent to read unstructured data. 
│   ├───main.py               # Application entry point. Creates an agent, creates a population_data tool, registers tools with the agent.
│   ├───note_engine.py        # Tool used by the agent to write notes in a notes.txt file.
│   └───prompts.py            # Prompt template used during Pandas queries.
├───Makefile                  # Make utility shortcuts.
├───poetry.lock               # File generated from pyproject.toml by poetry. Do not edit manually.
├───pyproject.toml            # Poetry dependencies file.
├───README.md                 # Documentation - you are reading it right now.
```


## Notes

- This is a proof of concept. As such, the application is not stable and prone to crushing. The main issue arises due to chatbot responses being non-deterministic and the application is not always able to deal with them appropriately.
- A further issue is that the agent does not always perform a complete search through its knowledge base. There are a number of ways this could be fixed including via further prompt engineering.
- It is possible to modify this application to use an LLM integrated into the application or to query a locally hosted agent. I have been able to integrate this application with `mistral 8x7b` and `llama2 7b` models hosted locally via [ollama](https://ollama.com/). 
For further documentation on ollama se [here](https://github.com/ollama/ollama). In my testing I found that stable integration with non-OpenAI models is much more limited on LlamaIndex compared to OpenAI models. 
Using `mistral` or `llama2` was significantly more likely to crush the application as they were both prone to selecting to use tools that did not exist.

### Using Ollama models

In this example I will use the ollama `mistral` model.
- Install [ollama](https://ollama.com/), then open CMD/Terminal and run `ollama run mistral`. This will start the ollama server and, download the 4GB model if this is your first time using the model, and then start a chat session. This also makes the model API available for querying.
- Run `poetry add llama-index-llms-ollama` in the root directory of rag-chatbot to install the ollama model wrapper.
- Add and run the following code in main.py to confirm connectivity with the model. Note: it may take around 30 seconds to receive the 1st response from the model as ollama will initiate a new session.
```python
from llama_index.llms.ollama import Ollama
llm = Ollama(model="llama2", request_timeout=30.0)
resp = llm.complete("What are the different categories of starts?")
print(resp)
```