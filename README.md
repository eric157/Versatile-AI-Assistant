# Versatile AI Assistant

A versatile AI assistant built using **Streamlit, Langchain, and Ollama**. This app provides a user-friendly interface for interacting with a large language model (LLM), allowing you to customize the system prompt, adjust the temperature, and manage chat sessions efficiently.

## Features

### 🔹 **LLM Model Support**
- Choose from various models: `deepseek-r1:1.5b`, `phi3`, `gemma2:2b`, and `stable-code`, each offering unique strengths.

### 🎭 **Customization Options**
- **Customizable System Prompt**: Tailor AI behavior with predefined instructions.
- **Adjustable Temperature Control**: Modify randomness using a temperature slider.
- **Response Length & Style**: Choose response length and style preferences.
- **AI Persona Selection**: Define the AI's personality (e.g., Friendly, Professional, Humorous).

### 💬 **Chat Interaction**
- **Streaming Responses**: Get real-time AI-generated responses with token count visibility.
- **Response Time Display**: View the time taken to generate responses.
- **Regenerate Response**: Easily request a new response for the last query.
- **User-Friendly Interface**: Enjoy a smooth chat experience with AI and user avatars.

### 📂 **Session & Data Management**
- **Chat Session Management**: Create, switch, rename, and delete chat sessions.
- **Quick Prompts**: Use preset prompts to start conversations effortlessly.
- **Response Speed Indicator**: Monitor AI response speed via a progress bar.
- **Feedback Mechanism**: Rate responses as Good, Neutral, or Bad.
- **Chat Export**: Save chat history as a text file.

---

## Installation Guide

### 1️⃣ **Clone the Repository**
```bash
git clone https://github.com/eric157/Versatile-AI-Assistant.git
cd Versatile-AI-Assistant
```

### 2️⃣ **Install Ollama**
- Follow the instructions on the [Ollama website](https://ollama.ai) to install Ollama.

### 3️⃣ **Download Required Models**
```bash
ollama run deepseek-r1:1.5b
ollama run phi3
ollama run gemma2:2b
ollama run stable-code
```
- Verify downloaded models:
```bash
ollama list
```

### 4️⃣ **Run the Model Server**
Start the Ollama model server in the background:
```bash
ollama run deepseek-r1:1.5b
```
*(Leave this terminal running to keep the Ollama server active.)*

### 5️⃣ **Install Project Dependencies**
```bash
pip install -r requirements.txt
```

### 6️⃣ **Run the Streamlit App**
```bash
streamlit run app.py
```
---

## Usage

### 📌 **Model Selection**
- Select an LLM model from the sidebar dropdown.

### 🎭 **System Prompt Customization**
- Choose AI response length, style, and persona using the sidebar options.

### 🔥 **Temperature Control**
- Adjust the temperature slider to control response randomness.

### 📁 **Chat Session Management**
- Create, switch, rename, and delete chat sessions via the sidebar.

### ⚡ **Quick Prompts**
- Start conversations using predefined prompts.

### 💬 **Chat Input & Responses**
- Enter queries in the chat input box and press **Enter**.
- Responses stream in real time, displaying token counts.

### ⏳ **Response Time & Speed Indicator**
- View response time below messages.
- Monitor speed using the progress bar.

### 🔄 **Regenerate Response**
- Click "Regenerate Response" to get a new AI response.

### 👍 **Feedback Mechanism**
- Rate AI responses via the sidebar feedback options.

### 📤 **Chat Export**
- Click "Export Chat" to save conversation logs as a text file.

---

## Troubleshooting

### 🛠 **Ollama Server Issues**
- Ensure the Ollama server is running with the selected model loaded.
- The app communicates with Ollama at `http://localhost:11434` by default.
- If the port is changed, update the `ollama_base_url` variable in `app.py`.

### 📌 **Model Availability**
- Run `ollama list` to verify installed models.

### ⚠ **Error Messages**
- Check the Streamlit app and Ollama server console for debugging hints.

### 🔄 **Performance Optimizations**
- Utilize `@st.cache_resource` for efficient caching of LLM instances.
- Stream responses for a better user experience.

---
