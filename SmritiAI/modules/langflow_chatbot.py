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
            except Exception as e:
                print("gTTS Error:", e)
                return None
        else:
            # Use pyttsx3 (offline) if gTTS fails
            try:
                engine.save_to_file(text, temp_file_path)
                engine.runAndWait()
            except Exception as e:
                print("pyttsx3 Error:", e)
                return None
    return temp_file_path

# Function to play the saved response audio
def play_audio(file_path):
    """Plays the generated speech audio."""
    try:
        sound = AudioSegment.from_file(file_path, format="mp3")
        play(sound)
    except Exception as e:
        print("Audio Playback Error:", e)

# SmritiAI Chatbot function with Whisper-based Voice Input and TTS Output
def chatbot_app_langflow():
    """Runs SmritiAI Chatbot inside Streamlit with voice input, TTS output, and replay button."""
    st.title("🧠 SmritiAI - Dementia Support Chatbot (Langflow)")

    # Toggle for voice output
    if "enable_voice" not in st.session_state:
        st.session_state.enable_voice = True

    st.session_state.enable_voice = st.sidebar.checkbox("🔊 Enable Voice Output", value=st.session_state.enable_voice)

    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Display chat history
    for role, message, audio_file in st.session_state.chat_history:
        with st.chat_message("user" if role == "You" else "assistant"):
            st.markdown(message)
            if audio_file:
                if st.button(f"▶️ Replay {role}'s Response", key=f"replay_{hash(message)}"):
                    play_audio(audio_file)

    # User input options
    col1, col2 = st.columns([2, 1])
    
    with col1:
        user_input = st.chat_input("Ask SmritiAI anything...")
        print(user_input)

    with col2:
        if st.button("🎤 Speak"):
            voice_text = record_voice_input()
            if voice_text:
                user_input = voice_text

    if user_input:
        # Append user message to chat history
        st.session_state.chat_history.append(("You", user_input, None))

        # Display user message
        with st.chat_message("user"):
            st.markdown(user_input)

        print(f"User Input is ----------------------------------------------------------------\n{user_input}")
        # Send request to Langflow
        response = send_to_langflow(user_input)
        print("this is response ---------------------------------------------------------------------")
        print(response)
        # Generate voice response if voice is enabled
        audio_file = None
        if st.session_state.enable_voice:
            audio_file = text_to_speech(response)
            play_audio(audio_file)  # Auto-play once

        # Append AI response to chat history
        st.session_state.chat_history.append(("🧠 SmritiAI", response, audio_file))

        # Display AI response
        with st.chat_message("assistant"):
            st.markdown(response)

# Run chatbot if script is executed
if __name__ == "__main__":
    chatbot_app_langflow()
