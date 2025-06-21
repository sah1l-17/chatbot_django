# ChatBot Django Master

A comprehensive web application that combines Django web framework with Streamlit-powered AI chatbots to help users learn programming concepts and analyze code. This project features user authentication, chat history management, and AI-powered code generation and analysis.

## About

ChatBot Django Master is an educational platform designed to help beginners learn programming in a simple and interactive manner. The application consists of two main components:

1. **Django Web Application**: Provides user authentication, registration, and navigation between different learning modules
2. **Streamlit Chatbots**: Two specialized AI-powered chatbots that offer:
   - **CodeCatalyst**: Helps users learn coding by generating code examples in C, Java, and Python, along with detailed explanations
   - **Code Analyzer**: Analyzes user-submitted code for time complexity, space complexity, and provides improvement suggestions

The platform is perfect for students who have just completed their 10th grade and want to start their coding journey, as well as anyone looking to improve their programming skills through AI-assisted learning.

## Features

- **User Authentication**: Secure signup and login system
- **Multi-language Code Generation**: Generate code examples in C, Java, and Python
- **Code Analysis**: Analyze code for complexity and get improvement suggestions
- **Chat History**: Persistent chat history with delete functionality
- **Responsive Design**: Clean and user-friendly interface
- **Database Integration**: SQLite database for storing user data and chat history

## Technology Stack

- **Backend**: Django 5.1
- **Frontend**: HTML, CSS, JavaScript
- **AI Integration**: Groq API with LLaMA 3.1 model
- **Chatbot Interface**: Streamlit
- **Database**: SQLite
- **Authentication**: Django's built-in authentication system

## Prerequisites

Before running this project, make sure you have the following installed:

- Python 3.8 or higher
- pip (Python package installer)
- Git (for cloning the repository)

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd chatbot_django-master
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\\Scripts\\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirement.txt
   ```

4. **Set up Groq API Key**
   - Create a `config.json` file in the `streamlit_chatbot` directory
   - Add your Groq API key:
   ```json
   {
     "GROQ_API_KEY": "your_groq_api_key_here"
   }
   ```

5. **Update database path** (if necessary)
   - Update the database path in `chatbot_django/settings.py`
   - Update the database path in `streamlit_chatbot/chatbot.py` and `streamlit_chatbot/practice.py`

## Running the Application

### 1. Start the Django Server

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

The Django application will be available at `http://127.0.0.1:8000/`

### 2. Start the Streamlit Chatbots

Open two separate terminal windows/tabs:

**For the Learning Chatbot (CodeCatalyst):**
```bash
cd streamlit_chatbot
streamlit run chatbot.py
```

**For the Code Analysis Chatbot:**
```bash
cd streamlit_chatbot
streamlit run practice.py
```

The Streamlit applications will typically run on:
- CodeCatalyst: `http://localhost:8501`
- Code Analyzer: `http://localhost:8502`

## Usage

1. **Registration/Login**: Start by creating an account or logging in through the Django web interface
2. **Learning Mode**: Navigate to the "Learn" section to access CodeCatalyst for code generation and explanations
3. **Practice Mode**: Use the "Practice" section to analyze your code and get improvement suggestions
4. **Chat History**: View and manage your previous conversations through the sidebar
5. **About**: Learn more about the platform and its features

## Project Structure

```
chatbot_django-master/
├── chatbot/                    # Django app
│   ├── templates/             # HTML templates
│   ├── models.py             # Database models
│   ├── views.py              # View functions
│   └── urls.py               # URL patterns
├── chatbot_django/           # Django project settings
│   ├── settings.py           # Project configuration
│   └── urls.py               # Main URL configuration
├── streamlit_chatbot/        # Streamlit applications
│   ├── chatbot.py           # Learning chatbot
│   ├── practice.py          # Code analysis chatbot
│   └── config.json          # API configuration
├── static/                   # Static files (CSS, images)
├── db.sqlite3               # SQLite database
├── manage.py                # Django management script
└── requirement.txt          # Python dependencies
```

## API Configuration

This project uses the Groq API for AI functionality. You'll need to:

1. Sign up for a Groq API account
2. Obtain your API key
3. Add it to the `config.json` file in the `streamlit_chatbot` directory

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## License

This project is open source and available under the [MIT License](LICENSE).

## Support

If you encounter any issues or have questions, please create an issue in the repository or contact the development team.

## Acknowledgments

- Groq for providing the AI API
- Django community for the excellent web framework
- Streamlit for the interactive chatbot interface
- LLaMA model for powering the AI responses

