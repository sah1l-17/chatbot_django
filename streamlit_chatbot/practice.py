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
        CREATE TABLE IF NOT EXISTS analysis (
            user_id TEXT,
            role TEXT,
            content TEXT,
            timestamp DATETIME
        )
    ''')
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    cursor.execute('INSERT INTO analysis (user_id, role, content, timestamp) VALUES (?, ?, ?, ?)', (user_id, 'user', user_message, current_time))
    cursor.execute('INSERT INTO analysis (user_id, role, content, timestamp) VALUES (?, ?, ?, ?)', (user_id, 'assistant', bot_response, current_time))
    
    conn.commit()
    conn.close()

# Load chat history for all prompts
def load_chat_history(user_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT rowid, role, content, timestamp FROM analysis WHERE user_id = ? ORDER BY timestamp ASC', (user_id,))
    messages = cursor.fetchall()
    conn.close()
    return messages

# Delete a specific chat history by rowid
def delete_chat_history(rowid):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM analysis WHERE rowid = ?', (rowid,))
    conn.commit()
    conn.close()

# Load Groq API key from config file
working_dir = os.path.dirname(os.path.abspath(__file__))
config_data = json.load(open(f"{working_dir}/config.json"))
GROQ_API_KEY = config_data["GROQ_API_KEY"]
os.environ["GROQ_API_KEY"] = GROQ_API_KEY
client = Groq()

# Function to analyze code using Ollama
def analyze_code_with_ollama(language, code):
    prompt = f"Analyze the following {language} code. Provide the time complexity, space complexity, and suggestions for improvement:\n\n{code}"
        
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "system", "content": prompt}]
    )
    
    # Extract the response content
    return response.choices[0].message.content

# Extract 'user_id' from URL parameters
query_params = st.experimental_get_query_params()
user_id = query_params.get('user_id', [None])[0]

# Check if the user is logged in via the user_id
if user_id:
    st.session_state['user_id'] = user_id
    previous_messages = load_chat_history(user_id)

# Dropdown menu to select programming language
language = st.selectbox("Select programming language", ("Python", "Java", "C"))

# Text area for code input
code = st.text_area(f"Enter your {language} code here", height=300)

# Button to run the code and fetch analysis
if st.button("Run"):
    if code:
        st.write("You entered:")
        if language == "Python":
            st.code(code, language='python')
        elif language == "Java":
            st.code(code, language='java')
        elif language == "C":
            st.code(code, language='c')

        # Call Ollama model to get the analysis
        analysis = analyze_code_with_ollama(language, code)
        
        # Display the analysis
        st.write("### Analysis")
        st.write(analysis)

        # Save interaction to the database
        save_chat_to_db(st.session_state['user_id'], code, analysis)
    else:
        st.write("Please enter some code to analyze.")

# Sidebar to show chat history with delete functionality
if "user_id" in st.session_state:
    st.sidebar.title("Chat History")
    chat_prompts = {}
    prompt_counter = 0
    for i, (rowid, role, content, timestamp) in enumerate(previous_messages):
        if role == "user":
            prompt_counter += 1
            
            # Extract a keyword for the sidebar, using the first line of the code or a unique identifier
            keyword = content.splitlines()[0] if content else "Code Prompt"
            chat_prompts[keyword] = previous_messages[i:i+2]
            
            # Display the chat history and add a delete button
            col1, col2 = st.sidebar.columns([4, 1])
            with col1:
                if col1.button(f"{keyword}", key=f"chat_{i}"):
                    st.session_state["selected_prompt"] = keyword
            with col2:
                if col2.button("🗑️", key=f"delete_{i}"):
                    delete_chat_history(rowid)
                    st.experimental_rerun()

# Display chat history for selected prompt
if "selected_prompt" in st.session_state:
    st.subheader(f"Chat Details for: {st.session_state['selected_prompt']}")
    selected_prompt_history = chat_prompts[st.session_state["selected_prompt"]]
    for role, content, timestamp in selected_prompt_history:
        st.write(f"**{role.capitalize()}** [{timestamp}]:\n{content}\n---")
