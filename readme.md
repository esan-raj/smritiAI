# SmritiAI - AI-Assisted Dementia Support System

SmritiAI is an AI-powered assistant designed to help individuals with dementia by providing personalized conversation support, reminders, and transcriptions. This project integrates Langflow, Streamlit, ChromaDB, and Twilio to enhance user experience and maintain conversational memory.

# Features

## 🧠 AI Chatbot (SmritiAI)

- AI-powered chatbot using Langflow

- Supports both text and voice input

- Conversational memory with ChromaDB for personalized responses

- Animated real-time subtitles synchronized with audio output

## 📝 Transcriber

- Converts speech to text

- Supports file uploads and live voice input

- Download transcriptions in DOCX or PDF format

## ✅ To-Do List with Reminders

- Create, manage, and store to-do tasks

- Automatically sets reminders for tasks with time specifications

- Sends SMS notifications using Twilio

## 🔔 Reminder System

- Detects reminders from user input (e.g., "Remind me at 5 PM")

- Converts AM/PM time format to 24-hour format dynamically

- Stores and retrieves reminders from a database

- Sends SMS alerts to users

## 📌 Dashboard Interface

- Unified navigation panel for Chatbot, Transcriber, and To-Do List

- Clean UI with dropdown menu for seamless interaction

- Settings to enable/disable voice output

- SmritiAI logo on the navigation panel


# Installation
## Prerequisites
Ensure you have the following installed:
- Python 3.10+
- Virtual Environment (recommended)
- Dependencies from `requirements.txt`

### Setup
```bash
# Clone the repository
git clone https://github.com/esan-raj/smritiAI.git
cd smritiAI

# Create a virtual environment
python -m venv env
source env/bin/activate  # On Windows use `env\Scripts\activate`

# Install dependencies
pip install -r requirements.txt
```
# Configurations
Create a .env file and add your Twilio credentials, database path, and other necessary keys:
```bash
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=your_twilio_number
DATABASE_PATH=reminders.db
GEMINI_API_KEY=your_gemini_api_key
```
# Running the Application
```bash
# Run the application
streamlit run main.py

# In another terminal 
langflow run
```
# Project Directory
```bash
SmritiAI/
│── main.py                 # Streamlit Dashboard
│── test.py                 # Testing script
│── requirements.txt        # Dependencies
├── modules/
│   ├── langflow_chatbot.py # Langflow chatbot integration
│   ├── reminder_manager.py # Handles reminders & SMS
│   ├── transcriber.py      # Speech-to-text module
│   ├── todo.py             # To-Do list with reminders
├── images/
│   ├── Smriti_ai_logo.jpg  # Project logo
├── workflows/
│   ├── Langflow Chatbot.json # Langflow configuration
└── chroma_db/              # Stores conversation history
```
# How it Works
1. **Chatbot Interaction**: Users can chat via text or voice.

2. **Memory & Personalization**: Past chats are stored using ChromaDB.

3. **Reminders & To-Do List**: Tasks with time details trigger reminders via Twilio SMS.

4. **Transcription Services**: Live and file-based transcriptions are available.

5. **Interactive UI**: A clean Streamlit-based dashboard for easy navigation.

# Future Improvements
- Support for multiple languages.

- More AI-powered cognitive assistance features.

- Integration with additional messaging platforms.

# 👥 Contributors

Thanks to these amazing people for their contributions! 🎉  

| Name           | Role                                      | GitHub Profile |
|---------------|------------------------------------------|----------------|
| **Esan Raj**  | Developer (Chatbot Development & Streamlit Integration) | [GitHub](https://github.com/esan-raj) |
| **Rahul Sanskar** | Developer (To-Do List)                  | [GitHub](https://github.com/Rahul-Sanskar) |
| **Aarti Jha** | Developer (Transcriber)                  | [GitHub](https://github.com/RT-Jha) |

---

## 🔥 Profile Avatars

[![Esan Raj](https://github.com/esan-raj.png?size=50)](https://github.com/esan-raj)
[![Rahul Sanskar](https://github.com/Rahul-Sanskar.png?size=50)](https://github.com/Rahul-Sanskar)
[![Aarti Jha](https://github.com/RT-Jha.png?size=50)](https://github.com/RT-Jha)

---

We appreciate all contributions to this project! 🚀✨


# License
**This project is licensed under the MIT License. Feel free to use and modify it!**

```bash
Let me know if you need any modifications! 🚀
