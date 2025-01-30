# Versatile AI Assistant

This is a versatile AI assistant built using Streamlit, Langchain, and Ollama. It provides a user-friendly interface for interacting with a large language model (LLM), allowing you to customize the system prompt and adjust the temperature. The app features streaming responses and displays the response time for each query.

---

## Features

- **Customizable System Prompt**: Set the initial instructions for the LLM to tailor its behavior.
- **Adjustable Temperature Control**: Control the randomness of the AI's responses using the temperature slider.
- **Streaming Responses**: Receive real-time feedback as the AI generates its response.
- **Response Time Display**: View the time taken to generate each response.
- **User-Friendly Chat Interface**: Interact with the AI through an intuitive chat interface.

---

## Installation

Follow these steps to set up and run the Versatile AI Assistant:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/eric157/Versatile-AI-Assistant.git
   cd Versatile-AI-Assistant
   ```

2. **Install Ollama**:
   - Follow the instructions on the [Ollama-website](https://ollama.com/) to install Ollama.

3. **Download the Model**:
   - After installing Ollama, download the required model using the following command:
     ```bash
     ollama pull deepseek-r1:1.5b
     ```

4. **Run the Model**:
   - Start the Ollama model server in the background:
     ```bash
     ollama run deepseek-r1:1.5b
     ```
   - Leave this terminal running to keep the Ollama server active.

5. **Install Project Dependencies**:
   - Install the required Python packages:
     ```bash
     pip install -r requirements.txt
     ```

6. **Run the Streamlit App**:
   - Start the Streamlit application:
     ```bash
     streamlit run app.py
     ```

---

## Usage

1. **System Prompt**:
   - Customize the AI's behavior by entering a system prompt in the sidebar. This sets the initial instructions for the LLM.

2. **Temperature**:
   - Adjust the temperature slider to control the randomness of the AI's responses. Lower temperatures result in more predictable outputs, while higher temperatures lead to more creative responses.

3. **Chat Input**:
   - Enter your query in the chat input box and press **Enter**.

4. **Streaming Responses**:
   - The AI's response will stream in real-time, providing immediate feedback.

5. **Response Time**:
   - The time taken to generate the response is displayed below the chat message.

---

## Troubleshooting

- **Ollama Server**:
  - Ensure the Ollama server is running and the model is loaded before starting the Streamlit app. The app communicates with Ollama at `http://localhost:11434` by default. If you've changed the Ollama port, update the `ollama_base_url` variable in `app.py`.

- **Model Availability**:
  - Confirm that the `deepseek-r1:1.5b` model has been successfully downloaded and is available to Ollama. Use `ollama list` to see available models.

- **Error Messages**:
  - Pay attention to any error messages displayed in the Streamlit app or the Ollama server console. These messages can provide valuable clues for debugging.