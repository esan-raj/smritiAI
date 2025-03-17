import streamlit as st
import whisper
import pyttsx3
import google.generativeai as genai
import speech_recognition as sr
import tempfile
import threading
import os

# Configure Gemini API
genai.configure(api_key="AIzaSyDGJl3XfCzixZzJAWsBx_Zv-V_gfhdUHvA")

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)

# Initialize Whisper model
whisper_model = whisper.load_model("base")

# Initialize speech recognition
recognizer = sr.Recognizer()
mic = sr.Microphone()

# Wake word
WAKE_WORD = "hey"

def listen_and_transcribe():
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        st.write("Listening...")
        try:
            audio = recognizer.listen(source)
            with tempfile.NamedTemporaryFile(delete=True, suffix=".wav") as temp_audio:
                temp_audio.write(audio.get_wav_data())
                temp_audio.flush()
                result = whisper_model.transcribe(temp_audio.name)
                return result['text'].lower()
        except Exception as e:
            return ""

def get_gemini_response(prompt):
    model = genai.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content(prompt)
    return response.text

def speak(text):
    engine.say(text)
    engine.runAndWait()

def wake_word_listener():
    while True:
        transcribed_text = listen_and_transcribe()
        print(transcribed_text)
        if WAKE_WORD in transcribed_text:
            st.write("Wake word detected! Listening for your question...")
            user_input = listen_and_transcribe()
            if user_input:
                st.session_state.chat_history.append(("You", user_input))
                chatbot_response = get_gemini_response(user_input)
                st.session_state.chat_history.append(("Chatbot", chatbot_response))
                speak(chatbot_response)

def main():
    st.title("Voice-Activated AI Chatbot")
    st.write("Say \"hey chatbot\" anytime to start speaking")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    # Start wake word listener in a separate thread
    threading.Thread(target=wake_word_listener, daemon=True).start()
    
    for role, message in st.session_state.chat_history:
        st.write(f"**{role}:** {message}")

if __name__ == "__main__":
    main()