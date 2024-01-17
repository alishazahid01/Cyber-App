# Import required libraries
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, AgentType
from langchain.callbacks import StreamlitCallbackHandler
from langchain.tools import DuckDuckGoSearchRun

# Set Streamlit page configuration
st.set_page_config(page_title="Cyber Chatbot", page_icon=":alien:", layout="wide")

# Create a sidebar for inputting OpenAI API key
with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")

# Create a container for the main title and introduction
with st.container():
    st.title("Hi, I am LLM Model 👋")
    st.subheader("A chatbot to help you in your cyber journey")
    st.write("I'm here to assist you in your cyber security journey. Feel free to ask any questions, anytime and anywhere! 😇")

# Create a container for displaying chat messages
with st.container():
    # Check if "messages" exist in session state, initialize if not
    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {"role": "assistant", "content": "Hi, How can I help you?"}
        ]

    # Display chat messages in the conversation
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    # Process user input and interact with the chatbot
    if prompt := st.chat_input(placeholder="Ask a Question! "):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        # Check if OpenAI API key is provided
        if not openai_api_key:
            st.info("Please add your OpenAI API key to continue.")
            st.stop()

        # Initialize chatbot model and search agent
        llm = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key=openai_api_key, streaming=True)
        search = DuckDuckGoSearchRun(name="Search")
        search_agent = initialize_agent([search], llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, handle_parsing_errors=True)

        # Generate response using the chatbot and display it
        with st.chat_message("assistant"):
            # Initialize Streamlit callback handler
            st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
            
            # Run the search agent to get the response
            response = search_agent.run(st.session_state.messages, callbacks=[st_cb])
            
            # Add the assistant's response to the conversation
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.write(response)
