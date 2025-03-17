import streamlit as st
import requests
import whisper
import numpy as np
import sounddevice as sd
import tempfile
import wave
import sys
import os
import time
import pyttsx3
import gtts
from pydub import AudioSegment
from pydub.playback import play
import requests
import asyncio
import re
from datetime import datetime
from modules.reminder_manager import add_reminder, get_reminders, remove_reminder, send_sms
import threading


# Load Whisper Model (Use 'base' for faster, 'small' or 'medium' for better accuracy)
MODEL_SIZE = "medium"
whisper_model = whisper.load_model(MODEL_SIZE)

# Initialize pyttsx3
engine = pyttsx3.init()
engine.setProperty("rate", 160)  # Adjust speech speed

# Langflow API settings
BASE_API_URL = "http://127.0.0.1:7860"
FLOW_ID = "9b4d72d9-6c80-4e27-962b-3120a9c0069e"  # Replace with your actual Flow ID

# Force model selection inside tweaks
TWEAKS = {
    "GoogleGenerativeAIModel-J8lcO": {"model_name": "gemini-1.5-pro"}
}

# Function to play a beep sound
def beep():
    """Plays a beep sound before and after recording starts."""
    if sys.platform == "win32":
        import winsound
        winsound.Beep(1000, 300)  # Beep at 1000 Hz for 300ms (Windows)
    else:
        fs = 44100  # Sampling frequency
        duration = 0.3  # 300ms beep
        t = np.linspace(0, duration, int(fs * duration), False)
        beep_sound = 0.5 * np.sin(2 * np.pi * 1000 * t)  # 1000 Hz sine wave
        sd.play(beep_sound, samplerate=fs)
        sd.wait()

# Function to record voice input and transcribe using Whisper
def record_voice_input():
    """Records voice input and transcribes it using Whisper."""
    st.info("🎙️ Beep! Speak now...")
    beep()  # Play beep before recording

    fs = 44100  # Sampling frequency
    duration = 8  # Maximum recording time in seconds
    st.info("🎙️ Recording... Speak now.")

    # Record audio
    audio_data = sd.rec(int(fs * duration), samplerate=fs, channels=1, dtype="int16")
    sd.wait()  # Wait until recording is finished

    beep()  # Play beep after recording ends
    st.success("✅ Recording complete. Transcribing...")

    # Save audio to temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
        temp_audio_path = temp_audio.name

        # Convert numpy array to WAV file
        with wave.open(temp_audio_path, "wb") as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(fs)
            wav_file.writeframes(audio_data.tobytes())

    # Transcribe audio using Whisper
    try:
        result = whisper_model.transcribe(temp_audio_path)
        os.remove(temp_audio_path)  # Delete temporary file after transcription
        text = result["text"].strip()
        if text:
            st.success(f"✅ Recognized: {text}")
            print(text)
            return text
        else:
            st.error("❌ No speech detected. Please try again.")
            return None
    except Exception as e:
        st.error(f"❌ Whisper transcription failed: {e}")
        return None

# Function to send user input to Langflow and get response
def send_to_langflow(user_input):
    """Sends user input to Langflow chatbot and retrieves AI response."""
    
    api_url = f"{BASE_API_URL}/api/v1/run/{FLOW_ID}"  # Ensure correct URL

    payload = {
        "input_value": user_input,  # Correct key expected by Langflow
        "output_type": "chat",      # Expected response type
        "input_type": "chat",       # Input mode
        "tweaks": TWEAKS            # Force Gemini model selection
    }

    try:
        response = requests.post(api_url, json=payload, headers={"Content-Type": "application/json"})
        
        if response.status_code == 200:
            data = response.json()
            # Extract the correct response from the API JSON
            outputs = data.get("outputs", [])
            if outputs and isinstance(outputs, list):
                first_output = outputs[0].get("outputs", [])
                if first_output and isinstance(first_output, list):
                    return first_output[0]["outputs"]["message"]["message"]
            return "⚠️ No valid response from SmritiAI."
        else:
            return f"⚠️ Error {response.status_code}: Unable to connect to Langflow API."

    except requests.exceptions.RequestException as e:
        return f"⚠️ API Error: {e}"

# Function to extract reminder details from user input
def extract_reminder_details(user_input):
    """
    Extracts reminder details (message and time) from user input.
    Converts AM/PM format to 24-hour format.
    """
    reminder_keywords = ["remind me", "schedule", "set a reminder"]
    time_patterns = [r"\b\d{1,2}:\d{2}\s?(AM|PM|am|pm)?\b", r"\bin\s\d+\s?(minutes|hours|days)\b"]

    if any(keyword in user_input.lower() for keyword in reminder_keywords):
        reminder_message = user_input
        reminder_time = None

        # Extract time if mentioned
        for pattern in time_patterns:
            match = re.search(pattern, user_input, re.IGNORECASE)
            if match:
                raw_time = match.group().strip()
                reminder_message = user_input.replace(raw_time, "").strip()

                # Convert 12-hour AM/PM format to 24-hour format
                try:
                    if "AM" in raw_time.upper() or "PM" in raw_time.upper():
                        reminder_time = datetime.strptime(raw_time, "%I:%M %p").strftime("%H:%M")
                    else:
                        reminder_time = datetime.strptime(raw_time, "%H:%M").strftime("%H:%M")
                except ValueError:
                    return None, None  # Invalid time format

                break
        
        return reminder_message, reminder_time
    return None, None

# Function to check if input contains a reminder request
def detect_and_set_reminder(user_input, phone_number):
    reminder_message, reminder_time = extract_reminder_details(user_input)
    if reminder_message and reminder_time:
        try:
            formatted_time = datetime.strptime(reminder_time, "%H:%M").strftime("%H:%M")
            add_reminder("User", reminder_message, formatted_time, phone_number)
            send_sms(phone_number, f"Reminder set: {reminder_message} at {formatted_time}")
            st.success(f"🔔 Reminder set: '{reminder_message}' at {formatted_time}")
            return True
        except ValueError:
            st.error("❌ Invalid time format. Use HH:MM (24-hour format).")
            return False
    return False


def manage_reminders(phone_number):
    reminders = get_reminders(phone_number)
    if not reminders:
        st.info("No upcoming reminders found.")
        return
    st.write("### 🔔 Upcoming Reminders")
    for reminder in reminders:
        reminder_id, user, message, reminder_time, phone = reminder
        st.write(f"📌 {message} at {reminder_time}")
        if st.button(f"❌ Remove", key=f"remove_{reminder_id}"):
            remove_reminder(reminder_id)
            st.success("Reminder removed!")
            st.rerun()


# Function to convert chatbot response to speech and save it
def text_to_speech(text, method="gtts"):
    """
    Convert text to speech using either Google TTS (gtts) or pyttsx3 (offline).
    Saves the audio file so it can be replayed.
    """
    temp_file_path = f"audio_responses/{hash(text)}.mp3"
    
    if not os.path.exists("audio_responses"):
        os.makedirs("audio_responses")

    if not os.path.exists(temp_file_path):
        if method == "gtts":
            try:
                tts = gtts.gTTS(text, lang="en")
                tts.save(temp_file_path)
                print("Audio file saved")
            except Exception as e:
                print("gTTS Error:", e)
                return None
        else:
            # Use pyttsx3 (offline) if gTTS fails
            try:
                engine.save_to_file(text, temp_file_path)
                engine.runAndWait()
                print("Audio file saved")
            except Exception as e:
                print("pyttsx3 Error:", e)
                return None
    return temp_file_path

# Function to play the saved response audio
def play_audio_with_highlight(file_path, text):
    """
    Plays the generated speech audio while highlighting words in sync.
    """
    try:
        sound = AudioSegment.from_file(file_path, format="mp3")
        words = text.split()
        duration_per_word = len(sound) / len(words)  # Approximate duration per word in milliseconds

        # Function to play audio in a separate thread
        def play_audio():
            play(sound)

        # Start playing audio in a separate thread
        audio_thread = threading.Thread(target=play_audio)
        audio_thread.start()

        # Display text with synchronized word highlighting
        for i, word in enumerate(words):
            highlighted_text = " ".join([
                f"<span style='background-color:yellow'>{w}</span>" if j == i else w
                for j, w in enumerate(words)
            ])
            st.markdown(f"<p style='font-size:18px'>{highlighted_text}</p>", unsafe_allow_html=True)
            time.sleep(duration_per_word / 1000.0)  # Convert ms to seconds

        # Ensure audio finishes playing
        audio_thread.join()

    except Exception as e:
        print("Audio Playback Error:", e)

# SmritiAI Chatbot function with Whisper-based Voice Input and TTS Output
def chatbot_app_langflow():
    """
    Runs SmritiAI Chatbot inside Streamlit with voice input, TTS output, and reminder detection.
    """
    st.title("🧠 SmritiAI - Dementia Support Chatbot (Langflow)")
    st.session_state.enable_voice = st.sidebar.checkbox("🔊 Enable Voice Output", value=True)

    # Phone number input for reminders
    if "phone_number" not in st.session_state:
        st.session_state.phone_number = ""
    phone_number = st.text_input("📱 Enter phone number for reminders:", value=st.session_state.phone_number, key="phone_input")
    if phone_number:
        st.session_state.phone_number = phone_number

    if st.sidebar.button("📅 View/Cancel Reminders"):
        manage_reminders(st.session_state.phone_number)

    # Display chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for chat_entry in st.session_state.chat_history:
        role, message, audio_file = chat_entry if len(chat_entry) == 3 else (chat_entry[0], chat_entry[1], None)
        with st.chat_message("user" if role == "You" else "assistant"):
            st.markdown(message)
            if audio_file:
                if st.button(f"▶️ Replay {role}'s Response", key=f"replay_{hash(message)}"):
                    play_audio_with_highlight(audio_file, message)

    # User input options
    col1, col2 = st.columns([2, 1])
    
    with col1:
        user_input = st.chat_input("Ask SmritiAI anything...", key="chat_input")

    with col2:
        if st.button("🎤 Speak"):
            voice_text = record_voice_input()
            if voice_text:
                user_input = voice_text

    if user_input:
        st.session_state.chat_history.append(("You", user_input))
        with st.chat_message("user"):
            st.markdown(user_input)

        # 🔔 Check if input is a reminder request
        reminder_message, reminder_time = extract_reminder_details(user_input)
        if reminder_message and reminder_time:
            if st.session_state.phone_number:
                add_reminder("User", reminder_message, reminder_time, st.session_state.phone_number)
                st.success(f"🔔 Reminder set: '{reminder_message}' at {reminder_time}")
                return
            else:
                st.error("❌ Please enter your phone number to set reminders!")

        # 🧠 Otherwise, send input to Langflow AI
        response = send_to_langflow(user_input)
        
        # 🎙️ Text-to-Speech + Subtitles
        audio_file = None
        if st.session_state.enable_voice:
            audio_file = text_to_speech(response)
        
        st.session_state.chat_history.append(("🧠 SmritiAI", response, audio_file))
        
        with st.chat_message("assistant"):
            st.markdown(response)
        
        if audio_file:
            play_audio_with_highlight(audio_file, response)

# Run chatbot if script is executed
if __name__ == "__main__":
    chatbot_app_langflow()