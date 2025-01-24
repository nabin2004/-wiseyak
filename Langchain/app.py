import streamlit as st
from agent import agent

# Streamlit UI
st.title("Search Agent with Groq and DuckDuckGo")
st.write("Ask me anything, and I'll search the web for you!")

query = st.text_input("Enter your query:", placeholder="What are the latest trends in data science in 2024?")

if query:
    with st.spinner("Searching and generating response..."):
        try:
            # Run the agent
            response = agent.run(query)
            st.success("Response:")
            st.write(response)
        except Exception as e:
            st.error(f"An error occurred: {e}")