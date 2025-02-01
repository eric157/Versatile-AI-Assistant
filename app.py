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
import os
import asyncio
from datetime import datetime
from typing import List, Dict, Any
from enum import Enum

# --- Helper functions ---
def load_local_image(image_name):
    image_path = os.path.join("images", image_name)
    try:
        return image_path
    except Exception as e:
        st.error(f"Error loading image: {image_name}. Error: {e}")
        return None

def get_avatar_for_role(role):
    if role == "user":
      return "👤"
    elif role == "ai":
      return "🤖"
    return "❓"

def calculate_token_count(text: str) -> int:
    # Basic approximation; adjust as needed for your specific model
    return len(text.split())

# Enums for choices
class ResponseLength(Enum):
    SHORT = "Short"
    MEDIUM = "Medium"
    LONG = "Long"

class ResponseStyle(Enum):
    FORMAL = "Formal"
    CASUAL = "Casual"
    TECHNICAL = "Technical"

class AIPersona(Enum):
    FRIENDLY = "Friendly"
    PROFESSIONAL = "Professional"
    HUMOROUS = "Humorous"

# --- End Helper Functions ---

# Session State Initialization
if "message_log" not in st.session_state:
    st.session_state.message_log = []
if "response_time" not in st.session_state:
    st.session_state.response_time = 0.0
if "chat_session_id" not in st.session_state:
    st.session_state.chat_session_id = 0
if "all_chat_logs" not in st.session_state:
    st.session_state.all_chat_logs = {0: []}
if "user_query" not in st.session_state:
    st.session_state.user_query = ""
if "session_names" not in st.session_state:
    st.session_state.session_names = {0: "Session 0"}

# App Title
st.title("Versatile AI Assistant")


# --- Load Images ---
# ... (load_local_image function remains the same)
# --- End Load Images ---

# Sidebar Configuration
available_models = {
    "deepseek-r1:1.5b": {"logo": "deepseek.png", "speciality": "Code focused LLM, good for software development and understanding"},
    "phi3": {"logo": "microsoft.png", "speciality": "Excellent general knowledge and reasoning capabilities, good at mathematics"},
    "gemma2:2b": {"logo": "gemma.png", "speciality": "Lightweight general-purpose model, good at following instructions and creative content generation"},
    "stable-code": {"logo": "stability-ai.png", "speciality": "Optimized for code generation, great at complex software engineering tasks"}
}

selected_model = st.sidebar.selectbox("Model", list(available_models.keys()), index=0)
model_info = available_models[selected_model]


with st.sidebar.container():
    st.markdown(f"**Model:** `{selected_model}`")
    col1, col2 = st.columns([1, 3])
    with col1:
        logo_path = load_local_image(model_info["logo"])
        if logo_path:
            st.image(logo_path, width=80, use_container_width=False)
    with col2:
        st.markdown(f"**Speciality:** {model_info['speciality']}")

temperature = st.sidebar.slider("Temperature", 0.0, 1.0, 0.3, 0.05)
response_length = st.sidebar.selectbox("Response Length", [e.value for e in ResponseLength], index=1)
response_style = st.sidebar.selectbox("Response Style", [e.value for e in ResponseStyle], index=0)
ai_persona = st.sidebar.selectbox("AI Persona", [e.value for e in AIPersona], index=0)
preset_prompts = {
    "Summarize Text": "Summarize this for me: ",
    "Explain Concept": "Explain this like I'm 5: ",
    "Generate Code": "Write Python code for: "
}
selected_preset = st.sidebar.selectbox("Quick Prompts", list(preset_prompts.keys()), index=None)
if selected_preset:
    st.session_state.user_query = preset_prompts[selected_preset]

# LLM Engine
@st.cache_resource
def get_llm_engine(model_name, base_url, temp):
    try:
        return ChatOllama(model=model_name, base_url=base_url, temperature=temp)
    except Exception as e:
        st.error(f"Error initializing model {model_name}: {e}")
        return None


ollama_base_url = "http://localhost:11434"
llm_engine = get_llm_engine(selected_model, ollama_base_url, temperature)
if llm_engine is None:
    st.stop()

# System Prompt
system_prompt_text = f"You are a helpful and informative AI assistant with a {response_style} style. You respond with a {response_length} length. You should act {ai_persona}."
system_prompt = SystemMessagePromptTemplate.from_template(system_prompt_text)

# Chat Session Management
def switch_chat_session(session_id):
    st.session_state.chat_session_id = session_id
    if session_id not in st.session_state.all_chat_logs:
         st.session_state.all_chat_logs[session_id] = []
    st.session_state.message_log = st.session_state.all_chat_logs[session_id]

def create_new_chat_session():
    new_session_id = max(st.session_state.all_chat_logs.keys()) + 1 if st.session_state.all_chat_logs else 1
    st.session_state.all_chat_logs[new_session_id] = []
    st.session_state.session_names[new_session_id] = f"Session {new_session_id}"
    switch_chat_session(new_session_id)

def delete_chat_session(session_id):
    del st.session_state.all_chat_logs[session_id]
    if session_id in st.session_state.session_names:
        del st.session_state.session_names[session_id]
    if st.session_state.chat_session_id == session_id:
        switch_chat_session(next(iter(st.session_state.all_chat_logs), 0))

def update_session_name(session_id):
    st.session_state.session_names[session_id] = st.session_state[f"session_name_{session_id}"]
    
def display_chat_messages():
     # Group messages by user and AI turns
    grouped_messages = []
    current_group = []
    last_role = None

    for message in st.session_state.message_log:
        if message["role"] != last_role and current_group:
            grouped_messages.append(current_group)
            current_group = []
        current_group.append(message)
        last_role = message["role"]
    if current_group:
        grouped_messages.append(current_group)
    for group in grouped_messages:
        with st.container():
          for message in group:
            with st.chat_message(message["role"], avatar=get_avatar_for_role(message["role"])):
                st.markdown(message["content"], unsafe_allow_html=True)
                if "timestamp" in message:
                    st.caption(message["timestamp"])

with st.sidebar.expander("Chat Sessions"):
    session_id_to_delete = None
    session_options = sorted(st.session_state.all_chat_logs.keys())
    selected_session_id = st.radio("Select Session", session_options,
                                   format_func=lambda session_id: f"{st.session_state.session_names.get(session_id, f'Session {session_id}')} {'*' if session_id == st.session_state.chat_session_id else ''}",
                                    index=session_options.index(st.session_state.chat_session_id) if st.session_state.chat_session_id in session_options else 0 )
    if selected_session_id != st.session_state.chat_session_id:
        switch_chat_session(selected_session_id)

    st.text_input("Edit Name", value=st.session_state.session_names.get(st.session_state.chat_session_id, f'Session {st.session_state.chat_session_id}'), key=f"session_name_{st.session_state.chat_session_id}",
                                     label_visibility="collapsed", on_change=update_session_name, args=[st.session_state.chat_session_id] )
    if st.button("Rename", key=f"rename_btn_{st.session_state.chat_session_id}", on_click=lambda id=st.session_state.chat_session_id: update_session_name(id)):
        pass
    if st.button("New Chat Session", on_click=create_new_chat_session):
        pass
    session_id_to_delete = st.selectbox("Delete Session",  sorted(st.session_state.all_chat_logs.keys()), index=None, format_func=lambda session_id: f"{st.session_state.session_names.get(session_id, f'Session {session_id}')}")
    if st.button("Delete", key="delete_btn", on_click=delete_chat_session, args=[session_id_to_delete]) if session_id_to_delete else False:
        pass

# Display Chat Messages
display_chat_messages()

# Chat Input and Processing
user_query = st.chat_input("Enter your query...", key="chat_input")

def build_prompt_chain():
    prompt_sequence = [system_prompt]
    for msg in st.session_state.message_log:
        if msg["role"] == "user":
            prompt_sequence.append(HumanMessagePromptTemplate.from_template(msg["content"]))
        elif msg["role"] == "ai":
            prompt_sequence.append(AIMessagePromptTemplate.from_template(msg["content"]))
    return ChatPromptTemplate.from_messages(prompt_sequence)

async def generate_ai_response(prompt_chain):
    full_response = ""
    message_placeholder = st.empty()
    processing_pipeline = prompt_chain | llm_engine | StrOutputParser()
    start_time = time.time()
    token_count_placeholder = st.empty()
    try:
        with st.spinner("AI is thinking..."):
            for chunk in processing_pipeline.stream({}):
                full_response += chunk
                message_placeholder.markdown(full_response + "▌")
                token_count_placeholder.caption(f"Token count: {calculate_token_count(full_response)}")

            message_placeholder.markdown(full_response)
            ai_response = full_response
            token_count_placeholder.caption(f"Token count: {calculate_token_count(full_response)}")
    except Exception as e:
          st.error(f"Error: {e}")
          ai_response = "Sorry, there was an issue processing your request."

    end_time = time.time()
    return ai_response, end_time - start_time


if user_query:
    st.session_state.message_log.append({"role": "user", "content": user_query, "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})

    with st.chat_message("ai", avatar=get_avatar_for_role("ai")):
        prompt_chain = build_prompt_chain()
        ai_response, response_time = asyncio.run(generate_ai_response(prompt_chain))

        st.session_state.response_time = response_time
        st.write(f"Response Time: {st.session_state.response_time:.2f} seconds")
        st.session_state.message_log.append({"role": "ai", "content": ai_response, "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
        st.session_state.all_chat_logs[st.session_state.chat_session_id] = st.session_state.message_log

        if st.button("Regenerate Response"):
            st.session_state.message_log.pop()
            st.rerun()
    st.session_state.user_query = ""
    st.rerun()

# Feedback Mechanism
feedback = st.sidebar.radio("How was the response?", ("Good", "Neutral", "Bad"))
if feedback:
    st.sidebar.write(f"Thank you for your feedback! You rated the response as: {feedback}")

# Response Speed Indicator
response_speed = st.sidebar.progress(0)
if st.session_state.response_time > 0:
    response_speed.progress(min(int(st.session_state.response_time * 10), 100))

# Export Chat Button
if st.sidebar.button("Export Chat"):
    chat_text = ""
    for msg in st.session_state.message_log:
      chat_text += f"{msg['role'].upper()} ({msg['timestamp']}): {msg['content']}\n"

    st.sidebar.download_button(
        label="Download Chat Log",
        data=chat_text,
        file_name="chat_log.txt",
        mime="text/plain"
    )