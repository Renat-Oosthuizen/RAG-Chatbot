from dotenv import load_dotenv
import os
import pandas as pd
from llama_index.experimental.query_engine import PandasQueryEngine
from llama_index.llms.openai import OpenAI
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.core.agent import ReActAgent
from prompts import new_prompt, instruction_str, context
from doc_reader import uk_engine, varied_engine
from note_engine import note_engine
from definitions import ROOT_DIR

load_dotenv()  # Load the API key from the .env file to connect to a remote agent

# Create the population_data tool
population_path = os.path.join(ROOT_DIR, "rag-chatbot", "data", "population.csv")
population_df = pd.read_csv(population_path)

population_query_engine = PandasQueryEngine(
    df=population_df, verbose=True, instruction_str=instruction_str
)
population_query_engine.update_prompts({"pandas_prompt": new_prompt})

# Register the tools with the agent
tools = [
    note_engine,
    QueryEngineTool(
        query_engine=population_query_engine,
        metadata=ToolMetadata(
            name="population_data",
            description="This has information at the world population and demographics.",
        ),
    ),
    QueryEngineTool(
        query_engine=uk_engine,
        metadata=ToolMetadata(
            name="uk_data",
            description="This has detailed information about United Kingdom.",
        ),
    ),
    QueryEngineTool(
        query_engine=varied_engine,
        metadata=ToolMetadata(
            name="varied_data",
            description="This has information the ages of characters in the Test the Chatbot show.",
        ),
    ),
]

# Create an agent from the specified LLM
llm = OpenAI(model="gpt-3.5-turbo-0613")
agent = ReActAgent.from_tools(tools, llm=llm, verbose=True, context=context)

# Create a loop allowing the user to query an agent or terminate the session
while (prompt := input("Enter a prompt (q to quit): ")) != "q":
    result = agent.query(prompt)
    print(result)
