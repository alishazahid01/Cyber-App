Cyber Chatbot Documentation

Introduction:

This repository contains the code for a Cyber Chatbot, which is a Streamlit-based application designed to assist users with questions related to cybersecurity. The chatbot leverages OpenAI's GPT-3.5 Turbo model to provide responses to user queries and performs searches using the DuckDuckGo Search API. This documentation provides an overview of the code and its functionality.
Getting Started

To run this chatbot, you need to follow these steps:

    Clone this repository to your local machine.
    Install the required dependencies. You can use the following command to install them:

	pip install -r requirements.txt

Obtain an OpenAI API key, which is required for interacting with the GPT-3.5 Turbo model.
Start the Streamlit application by running the following command:

    streamlit run main.py

    Access the chatbot in your web browser by navigating to the provided URL.

Code Structure:

The code for the Cyber Chatbot is organized into several sections, each with its specific functionality:
Importing Libraries

# Import required libraries
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, AgentType
from langchain.callbacks import StreamlitCallbackHandler
from langchain.tools import DuckDuckGoSearchRun

This section imports the necessary Python libraries and modules for building the chatbot, including Streamlit for the user interface and other custom modules for chatbot functionality.
Streamlit Configuration

# Set Streamlit page configuration
st.set_page_config(page_title="Cyber Chatbot", page_icon=":alien:", layout="wide")

Here, the Streamlit page configuration is set, including the title, page icon, and layout.
User Input and API Key


# Create a sidebar for inputting OpenAI API key
with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")

This section creates a sidebar in the Streamlit app where users can input their OpenAI API key. The input is masked for security.
Chatbot Introduction


# Create a container for the main title and introduction
with st.container():
    st.title("Hi, I am LLM Model 👋")
    st.subheader("A chatbot to help you in your cyber journey")
    st.write("I'm here to assist you in your cyber security journey. Feel free to ask any questions, anytime and anywhere! 😇")

In this part, a container is created to display the chatbot's title and introduction message.
Chat Messages


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

This section handles the display of chat messages. It initializes a conversation with a welcome message from the chatbot.
User Interaction


    # Process user input and interact with the chatbot
    if prompt := st.chat_input(placeholder="Ask a Question! "):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

Here, user input is processed, and the user's message is added to the conversation.
Chatbot Interaction


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

This is the core section where the chatbot interacts with the user. It checks if the OpenAI API key is provided, initializes the chatbot model, and generates responses based on user input. The responses are displayed in the chat interface.

Conclusion

This documentation provides an overview of the Cyber Chatbot code and its functionality. Users can interact with the chatbot by running the provided Streamlit application and providing their OpenAI API key. The chatbot uses OpenAI's GPT-3.5 Turbo model to provide responses and can perform searches using the DuckDuckGo Search API. Feel free to explore and customize this code for your own chatbot projects.
