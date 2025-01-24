from langchain_groq import ChatGroq
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.agents import initialize_agent, Tool, AgentType
import getpass
import os

# Set up Groq API key
if not os.environ.get("GROQ_API_KEY"):
    os.environ["GROQ_API_KEY"] = getpass.getpass("Enter API key for Groq: ")

# Initialize the Groq model
model = ChatGroq(model="llama3-8b-8192")

# Initialize the DuckDuckGo search tool
search_tool = DuckDuckGoSearchRun()

# Define a wrapper function to print search results
def search_and_print(query: str) -> str:
    print(f"Searching DuckDuckGo for: {query}")
    results = search_tool.run(query)
    print(f"Search Results:\n{results}\n")
    return results

# Define the tools
tools = [
    Tool(
        name="DuckDuckGo Search",
        func=search_and_print,  # Use the wrapper function
        description="Useful for searching the web for up-to-date information."
    )
]

# Initialize the agent
agent = initialize_agent(
    tools=tools,
    llm=model,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# # Query the agent
# query = "Generate the Pandas Interview questions?"
# response = agent.run(query)
# print(response)