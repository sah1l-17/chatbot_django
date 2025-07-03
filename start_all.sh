#!/bin/bash

echo "Starting Django server..."
python3 manage.py runserver &

echo "Starting CodeCatalyst Streamlit..."
streamlit run streamlit_chatbot/chatbot.py --server.port 8501 &

echo "Starting CodeAnalyzer Streamlit..."
streamlit run streamlit_chatbot/practice.py --server.port 8502 &
