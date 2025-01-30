import streamlit as st
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    AIMessagePromptTemplate,
    ChatPromptTemplate
)
import time

# Session state
if "message_log" not in st.session_state:
    st.session_state.message_log = [{"role": "ai", "content": "Hello! I'm your AI assistant."}]
if "response_time" not in st.session_state:
    st.session_state.response_time = 0.0

# App title
st.title("Versatile AI Assistant")

# Sidebar - Model and Temperature
selected_model = "deepseek-r1:1.5b"  # You can offer model choices later
st.sidebar.markdown(f"**Model:** `{selected_model}`")
temperature = st.sidebar.slider("Temperature", 0.0, 1.0, 0.3, 0.05)

# System Prompt -  More general purpose
system_prompt_text = st.sidebar.text_area("System Prompt", value="You are a helpful and informative AI assistant.")

# LLM Engine (cached)
@st.cache_resource  # Important for performance
def get_llm_engine(model_name, base_url, temp):
    return ChatOllama(model=model_name, base_url=base_url, temperature=temp)

ollama_base_url = "http://localhost:11434" #  Make sure this is correct
llm_engine = get_llm_engine(selected_model, ollama_base_url, temperature)


# System Prompt Template
system_prompt = SystemMessagePromptTemplate.from_template(system_prompt_text)

# Display Chat Messages
for message in st.session_state.message_log:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Chat Input and Processing
user_query = st.chat_input("Enter your query...")


def generate_ai_response(prompt_chain):
    processing_pipeline = prompt_chain | llm_engine | StrOutputParser()
    return processing_pipeline.invoke({})


def build_prompt_chain():
    prompt_sequence = [system_prompt]
    for msg in st.session_state.message_log:
        if msg["role"] == "user":
            prompt_sequence.append(HumanMessagePromptTemplate.from_template(msg["content"]))
        elif msg["role"] == "ai":
            prompt_sequence.append(AIMessagePromptTemplate.from_template(msg["content"]))
    return ChatPromptTemplate.from_messages(prompt_sequence)


if user_query:
    st.session_state.message_log.append({"role": "user", "content": user_query})

    with st.chat_message("ai"):
        message_placeholder = st.empty()
        full_response = ""
        start_time = time.time()
        processing_pipeline = build_prompt_chain() | llm_engine | StrOutputParser()
        try:
            for chunk in processing_pipeline.stream({}):  # Streaming response for better UX
                full_response += chunk
                message_placeholder.markdown(full_response + "▌") # Typing indicator
            message_placeholder.markdown(full_response)
            ai_response = full_response
        except Exception as e:
            st.error(f"Error: {e}")  # More concise error message
            ai_response = "Sorry, there was an issue processing your request."

        end_time = time.time()
        st.session_state.response_time = end_time - start_time
        st.write(f"Response Time: {st.session_state.response_time:.2f} seconds") # Moved inside 'ai' message

    st.session_state.message_log.append({"role": "ai", "content": ai_response})
    st.rerun() 