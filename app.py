import os
import time
import streamlit as st
from google import genai
from google.genai.errors import APIError

# Page Config
st.set_page_config(page_title="DoDo", page_icon="🦤", layout="centered")

# Custom Ultra-Clean CSS Injection
st.markdown("""
    <style>
    .stApp {
        background-color: #09090b;
        color: #fafafa;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    header {visibility: hidden;}
    footer {visibility: hidden;}

    textarea {
        background-color: #121215 !important;
        border: 1px solid #27272a !important;
        color: #f4f4f5 !important;
        border-radius: 12px !important;
        padding: 16px !important;
        font-size: 15px !important;
        line-height: 1.5 !important;
    }
    textarea:focus {
        border-color: #52525b !important;
        box-shadow: 0 0 0 1px #52525b !important;
    }

    .stButton>button {
        background-color: #fafafa !important;
        color: #09090b !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
        padding: 0.6rem 1.2rem !important;
        border: none !important;
        transition: all 0.2s ease !important;
        float: right;
    }
    .stButton>button:hover {
        background-color: #e4e4e7 !important;
        transform: translateY(-1px);
    }

    .output-container {
        background-color: #0f0f12;
        border: 1px solid #1e1e24;
        border-radius: 12px;
        padding: 20px;
        margin-top: 20px;
        color: #d4d4d8;
        font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
        font-size: 14px;
        line-height: 1.6;
    }
    </style>
""", unsafe_allow_html=True)

# Explicitly pull the API key from Streamlit secrets
try:
    if "GEMINI_API_KEY" in st.secrets:
        os.environ["GEMINI_API_KEY"] = st.secrets["GEMINI_API_KEY"]
except Exception:
    pass

# Initialize GenAI Client explicitly using the key from secrets
api_key = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# Header Layout
st.markdown("### 🦤 DoDo")
st.markdown("<p style='color: #71717a; font-size: 14px; margin-top: -10px;'>The elite execution engine. Drop text or speak your mind, get the solution.</p>", unsafe_allow_html=True)

# Input Tabs: Text vs Voice
tab_text, tab_voice = st.tabs(["✍️ Type / Paste", "🎙️ Record Audio"])

user_input = ""
audio_file = None

with tab_text:
    user_input = st.text_area(
        "Input",
        placeholder="Drop anything here... a messy transcript, a broken log, a raw idea, or a client brief.",
        height=160,
        label_visibility="collapsed"
    )

with tab_voice:
    st.markdown("<p style='color: #a1a1aa; font-size: 13px;'>Record your chaotic thoughts or voice notes directly:</p>", unsafe_allow_html=True)
    audio_file = st.audio_input("Record voice note", label_visibility="collapsed")

# Execution Action
if st.button("Execute Solution ⚡"):
    system_prompt = """
    You are DoDo, an elite, high-speed execution engine designed to deliver immediate, weaponized solutions. 
    Do not chat. Do not offer pleasantries. Do not explain what you did. 
    Analyze the input (whether text or transcribed audio), determine the exact problem it represents, and output ONLY the final, structured, pristine solution ready for immediate use.
    """

    models_to_try = ['gemini-3.5-flash', 'gemini-3.1-flash-lite']
    response = None
    success = False

    try:
        with st.spinner("Processing execution pipeline..."):
            for model_name in models_to_try:
                try:
                    if audio_file is not None:
                        with open("temp_audio.wav", "wb") as f:
                            f.write(audio_file.getbuffer())
                        
                        uploaded_audio = client.files.upload(
                            file="temp_audio.wav",
                            config={'mime_type': 'audio/wav'}
                        )
                        
                        response = client.models.generate_content(
                            model=model_name,
                            contents=[uploaded_audio, system_prompt]
                        )
                    elif user_input.strip():
                        response = client.models.generate_content(
                            model=model_name,
                            contents=f"{system_prompt}\n\nInput:\n{user_input}"
                        )
                    else:
                        st.warning("Please provide text or record an audio note first.")
                        st.stop()
                    
                    success = True
                    break # Break out of loop if successful
                except APIError as api_err:
                    if api_err.code in [503, 429]:
                        continue # Try the next backup model
                    else:
                        raise api_err

            if success and response:
                st.markdown("#### Solution Output")
                st.markdown(f'<div class="output-container">{response.text}</div>', unsafe_allow_html=True)
            else:
                st.error("All available model instances are currently under heavy load (503). Please wait a moment and try again.")

    except APIError as e:
        st.error(f"API Execution failed: {e}")
    except Exception as e:
        st.error(f"Execution failed: {e}")