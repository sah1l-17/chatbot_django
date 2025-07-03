import streamlit as st
import sqlite3
from datetime import datetime
import json
import os
from groq import Groq
from pathlib import Path


# Define BASE_DIR as project root
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "db.sqlite3"

# Load Groq API key from config file
CONFIG_PATH = Path(__file__).resolve().parent / "config.json"
with open(CONFIG_PATH, "r") as f:
    config_data = json.load(f)

GROQ_API_KEY = config_data["GROQ_API_KEY"]
os.environ["GROQ_API_KEY"] = GROQ_API_KEY

client = Groq()

# Database setup
def save_chat_to_db(user_id, user_message, bot_response):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chats (
            user_id TEXT,
            role TEXT,
            content TEXT,
            timestamp DATETIME
        )
    ''')
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    cursor.execute('INSERT INTO chats (user_id, role, content, timestamp) VALUES (?, ?, ?, ?)', (user_id, 'user', user_message, current_time))
    cursor.execute('INSERT INTO chats (user_id, role, content, timestamp) VALUES (?, ?, ?, ?)', (user_id, 'assistant', bot_response, current_time))
    
    conn.commit()
    conn.close()

# Load chat history for all prompts
def load_chat_history(user_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT rowid, role, content, timestamp FROM chats WHERE user_id = ? ORDER BY timestamp ASC', (user_id,))
    messages = cursor.fetchall()
    conn.close()
    return messages

# Delete a specific chat history by rowid
def delete_chat_history(rowid):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM chats WHERE rowid = ?', (rowid,))
    conn.commit()
    conn.close()


# Function to generate code in C, Java, and Python
def generate_code_for_languages(user_input):
    prompt = f"I have just completed my 10th and want to learn coding. Please provide the implementation of the following functionality in three languages: C, Java, and Python.\nFunctionality: {user_input}. Explain briefly each line of the code for each language."
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "system", "content": prompt}]
    )
    return response.choices[0].message.content

# Extract 'user_id' from URL parameters
query_params = st.experimental_get_query_params()
user_id = query_params.get('user_id', [None])[0]

# Check if the user is logged in via the user_id
if user_id:
    st.session_state['user_id'] = user_id
    previous_messages = load_chat_history(user_id)

# Chatbot UI
st.title('CodeCatalyst - Helping you learn code in the simplest manner')

# Sidebar to show prompts as buttons and delete option
if "user_id" in st.session_state:
    st.sidebar.title("Chat History")
    
    # Dictionary to hold chat prompts and their history
    chat_prompts = {}

    # Extract unique user prompts from the history
    for i, (rowid, role, content, timestamp) in enumerate(previous_messages):
        if role == "user":
            # Store each user prompt and its associated chat history
            chat_prompts[content] = previous_messages[i:i+2]  # Grab both user and assistant message
            
            # Create a layout for the chat prompt with a delete button
            col1, col2 = st.sidebar.columns([4, 1])
            with col1:
                # Sidebar button for each chat prompt
                if st.sidebar.button(f"{content}", key=f"chat_{i}"):
                    # Store the selected prompt in session state to display on the main page
                    st.session_state["selected_prompt"] = content
            with col2:
                # Sidebar delete button for each chat prompt
                if st.sidebar.button("🗑️", key=f"delete_{i}"):
                    # Delete the selected chat history and refresh the page
                    delete_chat_history(rowid)
                    st.experimental_rerun()

# Main input area
if "user_id" in st.session_state:
    input_text = st.text_input("Ask your question!", key="input_text_field")

    if input_text:
        if "messages" not in st.session_state:
            st.session_state["messages"] = []

        st.session_state["messages"].append({"role": "user", "content": input_text})

        # Check if the prompt is related to code
        if any(keyword in input_text.lower() for keyword in ["code", "script", "program"]):
            # Dynamically generate code in C, Java, and Python using the LLaMA model
            code_prompt = f"Please provide the implementation of the following functionality in three languages: C, Java, and Python.\nFunctionality: {input_text}"

            # Ask the Groq model to generate code in all three languages
            response_content = generate_code_for_languages(input_text)
        
        elif "result" in input_text:
            content = load_chat_history(user_id)
            result_prompt = f"Please summarize the following conversation history with you :{content}. Focus on the main topics discussed, any user questions, responses from the chatbot, and key insights or outcomes from the interactions."
            response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": result_prompt}]
            )
            response_content = response.choices[0].message.content
        else:
            # Generate a normal response
            general_prompt = f"You are a helpful assistant. Answer the following question: {input_text}"
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": general_prompt}]
            )
            response_content = response.choices[0].message.content

        # Save the new interaction to the database
        save_chat_to_db(st.session_state['user_id'], input_text, response_content)

        # Display the response
        st.write(f"Assistant: {response_content}")

# Display chat history for selected prompt on the main page
if "selected_prompt" in st.session_state:
    st.subheader(f"Chat Details for: {st.session_state['selected_prompt']}")
    
    # Get the selected chat history and display it
    selected_prompt_history = chat_prompts[st.session_state["selected_prompt"]]
    for role, content, timestamp in selected_prompt_history:
        st.write(f"**{role.capitalize()}** [{timestamp}]:\n{content}\n---")
