import streamlit as st
import speech_recognition as sr
from fpdf import FPDF
from datetime import datetime

# Streamlit page config
st.set_page_config(page_title="Anesthesia Voice Recorder", layout="wide")

st.title("🛌 Voice-Activated Anesthesia Documentation System")

# Session state init
if "recording" not in st.session_state:
    st.session_state.recording = False
if "transcript" not in st.session_state:
    st.session_state.transcript = []
if "final_transcript" not in st.session_state:
    st.session_state.final_transcript = ""

# 🎙 Voice recorder
def listen_and_transcribe():
    r = sr.Recognizer()
    mic = sr.Microphone()

    st.info("🎙 Listening... You can speak for up to 30 minutes. Press Stop to end.")
    with mic as source:
        # Adjust for ambient noise for better transcription
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source, timeout=None, phrase_time_limit=1800)  # 30 minutes

    try:
        result = r.recognize_google(audio)
        st.session_state.transcript.append(result)
        st.success(f"🗣 Transcribed: {result}")
    except sr.UnknownValueError:
        st.warning("❗ Could not understand the audio")
    except sr.RequestError:
        st.error("🔌 Network/API Error")

# 🎛 Layout: Admin, Patient, Encounter
tabs = st.tabs(["🧑‍⚕ Admin Info", "🧍 Patient Info", "❤ Vitals", "💊 Medications", "🗣 Notes"])

with tabs[0]:
    st.subheader("🧑‍⚕ Admin Info")
    anesthesiologist = st.text_input("Anesthesiologist Name")
    date = st.date_input("Date", value=datetime.today())
    or_number = st.text_input("OR Number")
    hospital = st.text_input("Hospital")

with tabs[1]:
    st.subheader("🧍 Patient Info")
    patient_name = st.text_input("Patient Name")
    age = st.text_input("Age")
    sex = st.radio("Sex", ["Male", "Female", "Other"], horizontal=True)
    procedure = st.text_input("Surgery/Procedure")
    mrn = st.text_input("MRN / Patient ID")

with tabs[2]:
    st.subheader("❤ Vitals (Real-Time or Dictated)")
    vitals_summary = st.text_area("Vitals Notes (BP, HR, SpO2, RR, Temp)", height=100)

with tabs[3]:
    st.subheader("💊 Medications Administered")
    medication_log = st.text_area("Medications, Dose, Time", height=100)

with tabs[4]:
    st.subheader("🗣 Free Voice Notes")
    live_notes = "\n".join(st.session_state.transcript)
    st.text_area("Live Transcript", value=live_notes, height=200, key="final_transcript")

# 🎙 Voice Recording Controls
col1, col2 = st.columns(2)
with col1:
    if st.button("▶ Start Voice Recording"):
        st.session_state.recording = True
with col2:
    if st.button("⏹ Stop Recording"):
        st.session_state.recording = False

# Run recorder loop only if recording
if st.session_state.recording:
    listen_and_transcribe()

# 📄 PDF generation function
def generate_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    def section(title, content):
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(200, 10, title, ln=True)
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, content)
        pdf.ln(4)

    section(" Admin Info", f"Name: {anesthesiologist}\nDate: {date}\nHospital: {hospital}\nOR: {or_number}")
    section(" Patient Info", f"Name: {patient_name}\nAge: {age}\nSex: {sex}\nMRN: {mrn}\nProcedure: {procedure}")
    section(" Vitals", vitals_summary)
    section(" Medications", medication_log)
    section(" Voice Notes", "\n".join(st.session_state.transcript))

    file_path = "anesthesia_record.pdf"
    pdf.output(file_path)
    return file_path

# 📤 Generate PDF button
if st.button("📄 Generate Report"):
    pdf_file = generate_pdf()
    with open(pdf_file, "rb") as f:
        st.download_button("⬇ Download Anesthesia Record", f, file_name="anesthesia_record.pdf", mime="application/pdf")
# ------------------ Footer ------------------
st.markdown("""
---
<div style='text-align: center; color: gray;'>
<strong>© 2025 | Designed & Owned by Janhavi Jangam</strong>
</div>
""", unsafe_allow_html=True)