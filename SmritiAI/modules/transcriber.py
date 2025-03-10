import streamlit as st
import sounddevice as sd
import wavio
import numpy as np
import whisper
import tempfile
from docx import Document
from fpdf import FPDF

# Function to record live audio
def record_audio(duration=5, samplerate=44100):
    st.write("🎤 Recording... Speak now!")
    audio_data = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=1, dtype=np.int16)
    sd.wait()
    st.write("✅ Recording finished!")

    # Save as WAV
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    wavio.write(temp_file.name, audio_data, samplerate, sampwidth=2)
    return temp_file.name

# Function to save transcript as DOCX
def save_as_docx(transcript):
    doc = Document()
    doc.add_paragraph(transcript)
    temp_path = tempfile.NamedTemporaryFile(delete=False, suffix=".docx").name
    doc.save(temp_path)
    return temp_path

# Function to save transcript as PDF
def save_as_pdf(transcript):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, transcript)
    temp_path = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf").name
    pdf.output(temp_path)
    return temp_path

# Transcriber function
def transcriber_app():
    st.title("🎙️ AI Transcriber (File & Live Audio)")

    transcriber_mode = st.radio("Choose Input Method:", ["📂 Upload File", "🎤 Live Recording"])

    transcript_text = None  # Store the transcript

    if transcriber_mode == "📂 Upload File":
        uploaded_file = st.file_uploader("Upload an audio file", type=["mp3", "wav", "m4a"])
        if uploaded_file:
            st.audio(uploaded_file, format="audio/mp3")
            temp_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3").name
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.read())
            
            # Load Whisper and transcribe
            model = whisper.load_model("base")
            result = model.transcribe(temp_path)
            transcript_text = result["text"]
            st.success(f"📜 **Transcription:** {transcript_text}")

    elif transcriber_mode == "🎤 Live Recording":
        duration = st.slider("Select recording duration (seconds)", 3, 20, 5)
        if st.button("🎤 Start Recording"):
            audio_path = record_audio(duration)
            st.audio(audio_path, format="audio/wav")

            # Load Whisper and transcribe
            model = whisper.load_model("base")
            result = model.transcribe(audio_path)
            transcript_text = result["text"]
            st.success(f"📜 **Transcription:** {transcript_text}")

    # Download Options for Transcript
    if transcript_text:
        st.write("### 📥 Download Transcript")
        
        # Save transcript as DOCX
        docx_path = save_as_docx(transcript_text)
        with open(docx_path, "rb") as docx_file:
            st.download_button(label="📄 Download as DOCX", data=docx_file, file_name="transcript.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")

        # Save transcript as PDF
        pdf_path = save_as_pdf(transcript_text)
        with open(pdf_path, "rb") as pdf_file:
            st.download_button(label="📝 Download as PDF", data=pdf_file, file_name="transcript.pdf", mime="application/pdf")
