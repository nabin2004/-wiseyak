from langgraph.graph import StateGraph, START, END 
from typing import Annotated
from typing_extensions import TypedDict 
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from IPython.display import Image, display

model = "MODEL HERE"

class State(TypedDict):
    messages: Annotated[list, add_messages]

graph_builder = StateGraph(State)


### NODES #############
def chatbot(state: State):
    pass

def extract_keywords(state: State):
    pass 

def search_db(state: State):
    pass 

def pandas_docs_search(state: State):
    pass 

def generate_LLM_questions(sate: State):
    pass 

def human_feedback(state: State):
    pass

def refactor_question(state: State):
    pass

def save_to_db(state: State):
    pass



## Conditional function
def check_approval(state: State):
    pass 

def check_existance(state: State):
    pass 


### NODES ENDS HERE ########

### TOOOOOOLS



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
graph_builder.add_edge('chatbot','extract_keywords')

graph_builder.add_conditional_edges(
    "extract_keywords",
    check_existance, 
    {
        "have_10_questions_already": "human_feedback",
        "no_questions": "pandas_docs_search",
    }
)

graph_builder.add_edge('pandas_docs_search','generate_LLM_questions')
graph_builder.add_edge('generate_LLM_questions','human_feedback')
graph_builder.add_conditional_edges(
    "human_feedback",
    check_approval, 
    {
        "Need Refactoring": "refactor_question", 
        "Satisfactory": 'save_to_db',  
    },
)
graph_builder.add_edge('save_to_db',END)
graph_builder.add_edge('refactor_question','human_feedback')


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
