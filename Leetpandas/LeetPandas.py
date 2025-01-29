from bs4 import BeautifulSoup
from langgraph.graph import StateGraph, START, END 
from typing import Annotated
from typing_extensions import TypedDict 
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from IPython.display import Image, display
from langchain_groq import ChatGroq
import os 
import getpass
import requests

if not os.environ.get("GROQ_API_KEY"):
    os.environ["GROQ_API_KEY"] = getpass.getpass("Enter API key for Groq: ")

model = ChatGroq(model="llama3-8b-8192")

class State(TypedDict):
    messages: Annotated[list, add_messages]
    keywords: list
    questions: list 
    question: str 

graph_builder = StateGraph(State)


### NODES #############
def chatbot(state: State):
    response = model.invoke(state["messages"]) 
    return {"messages":[{"role": "assistant", "content": response.content}]}

def extract_keywords(state: State):
    text = state["messages"][-1]["content"]
    prompt = f"Extract the most relevant keywords from the following text: {text}"
    response = model.invoke({"prompt": prompt, "max_tokens": 50})
    keywords = response.content.split(',')  
    return {"keywords": keywords}

def search_db(state: State):
    # Mock implementation for now
    return {"questions": []}

def pandas_docs_search(state: State, query: str):
    url = "https://pandas.pydata.org/pandas-docs/stable/search.html?q="
    search_url = url + query
    response = requests.get(search_url)
    if response.status_code != 200:
        return {"error": "Failed to retrieve documentation"}
    soup = BeautifulSoup(response.text, 'html.parser')
    results = soup.find_all('li', class_='searchresult')
    
    result_data = []
    for result in results:
        title = result.find('a').text.strip()
        url = result.find('a')['href']
        result_data.append({"title": title, "url": url})
    return result_data

def generate_LLM_questions(state: State, result_data: list):
    text_to_use = "\n".join([f"Title: {item['title']}\nURL: {item['url']}" for item in result_data])
    prompt = f"Generate a set of interview-style questions based on the following documentation content:\n{text_to_use}"
    response = model.invoke({"prompt": prompt, "max_tokens": 150})
    questions = response.content.strip().split("\n")
    return {"questions": questions}
    
def human_feedback(state: State):
    answer = input("Are AI-generated questions satisfactory? (Yes/No): ")
    if answer.lower() == "yes":
        return "Satisfactory"
    else: 
        return "Need Refactoring"
        
        
def refactor_question(state: State):
    question = state.get("question", "")
    if not question:
        return {"error": "No question provided in the state"}

    prompt = f"Please improve and enrich the following question, making it clearer and more engaging: '{question}'"
    response = model.invoke({"prompt": prompt, "max_tokens": 100})
    enriched_question = response.content.strip()
    return {"refactored_question": enriched_question}


def save_to_db(state: State):
    # Mock implementation for now
    print("Questions saved to database.")
    return {"status": "success"}


## Conditional function
def check_approval(state: State):
    feedback = state.get("feedback", "")
    return feedback

def check_existance(state: State):
    questions = state.get("questions", [])
    if len(questions) >= 10:
        return "have_10_questions_already"
    else:
        return "no_questions"

### NODES ENDS HERE ########



### GRAPH STARTS HERE

## Nodes
graph_builder.add_node("chatbot",chatbot)
graph_builder.add_node("extract_keywords",extract_keywords)
graph_builder.add_node('search_db',search_db)
graph_builder.add_node("pandas_docs_search",pandas_docs_search)
graph_builder.add_node("generate_LLM_questions",generate_LLM_questions)
graph_builder.add_node("human_feedback",human_feedback)
graph_builder.add_node("refactor_question",refactor_question)
graph_builder.add_node("save_to_db",save_to_db)


## Edges
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge('chatbot', 'extract_keywords')
graph_builder.add_edge('extract_keywords', 'search_db')
graph_builder.add_conditional_edges(
    "search_db",
    check_existance, 
    {
        "have_10_questions_already": "human_feedback",
        "no_questions": "pandas_docs_search",
    }
)

graph_builder.add_edge('pandas_docs_search', 'generate_LLM_questions')
graph_builder.add_edge('generate_LLM_questions', 'human_feedback')
graph_builder.add_conditional_edges(
    "human_feedback",
    check_approval, 
    {
        "Need Refactoring": "refactor_question", 
        "Satisfactory": 'save_to_db',  
    },
)
graph_builder.add_edge('save_to_db', END)
graph_builder.add_edge('refactor_question', 'human_feedback')


### GRAPH ENDS HERE

graph = graph_builder.compile()

# Generate the graph image
png_image = graph.get_graph().draw_mermaid_png()

# Display the image (optional)
display(Image(png_image))

# Save the image to a file
with open("Leetpandas/graph_output.png", "wb") as file:
    file.write(png_image)

print("Image saved as 'graph_output.png'")