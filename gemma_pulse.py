import streamlit as st
import json
import os
import plotly.express as px
import ollama
from streamlit_mic_recorder import mic_recorder
import pandas as pd
from datetime import datetime

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Gemma-Pulse | Clinical Terminal",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. ADVANCED CSS & ANIMATIONS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Plus+Jakarta+Sans:wght@300;400;600;800&display=swap');

    :root {
        --primary: #3b82f6;
        --accent: #10b981;
        --bg-dark: #020617;
        --card-bg: rgba(30, 41, 59, 0.7);
    }

    .stApp {
        background: radial-gradient(circle at 0% 0%, #0f172a 0%, #020617 100%);
        color: #f8fafc;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* Glassmorphism Header */
    .header-container {
        padding: 1.5rem;
        background: var(--card-bg);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 2rem;
        text-align: left;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .main-header { 
        font-size: 2.5rem; 
        font-weight: 800; 
        background: linear-gradient(90deg, #60a5fa, #34d399); 
        -webkit-background-clip: text; 
        -webkit-text-fill-color: transparent;
        margin: 0;
    }

    /* Metric Cards */
    [data-testid="stMetricValue"] { font-family: 'JetBrains Mono', monospace; color: #60a5fa !important; }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #0f172a !important;
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }

    /* Chat Styling */
    .stChatMessage {
        border-radius: 15px !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        padding: 1rem;
        margin-bottom: 1rem !important;
    }

    /* Quick Action Buttons */
    .stButton>button {
        border-radius: 10px;
        text-transform: uppercase;
        font-weight: 600;
        letter-spacing: 0.5px;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. ENGINE LOGIC ---
class GemmaPulseEngine:
    def __init__(self, model="pdurlej/gemma-4-26B-A4B-it-heretic:Q4_K_M"): 
        self.model = model

    def process_input(self, text_input, history, patient_context):
        system_prompt = (
            f"You are Gemma-Pulse, a professional clinical assistant. "
            f"CURRENT PATIENT CONTEXT: {patient_context}. "
            "Prioritize triage accuracy, drug interaction warnings, and brevity."
        )
        messages = [{"role": "system", "content": system_prompt}] + history
        messages.append({"role": "user", "content": text_input})
        
        try:
            response = ollama.chat(model=self.model, messages=messages)
            return response['message']['content']
        except Exception as e:
            return f"❌ Connection Error: {str(e)}"

# --- 4. INITIALIZATION & DATA ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "voice_active" not in st.session_state:
    st.session_state.voice_active = False

engine = GemmaPulseEngine()

# --- 5. SIDEBAR: CLINICAL DASHBOARD ---
with st.sidebar:
    st.markdown("<h2 style='color: #60a5fa;'>🩺 CLINICAL HUB</h2>", unsafe_allow_html=True)
    
    # Patient Context Form
    with st.expander("👤 PATIENT CONTEXT", expanded=True):
        p_id = st.text_input("Patient ID", value="PX-4402")
        p_age = st.number_input("Age", 0, 120, 45)
        p_sex = st.selectbox("Sex", ["Male", "Female", "Other"])
        p_hx = st.text_area("Known History", "Hypertension, Type II Diabetes")
        context_str = f"ID: {p_id}, Age: {p_age}, Sex: {p_sex}, History: {p_hx}"

    st.divider()
    
    # Inventory Health
    st.markdown("### 📦 INVENTORY STATUS")
    col1, col2 = st.columns(2)
    col1.metric("Insulin", "8 units", "-20%", delta_color="inverse")
    col2.metric("Bandages", "45", "Normal")
    
    # Quick Inventory Viz
    items_df = pd.DataFrame({
        "Item": ["Paracetamol", "Insulin", "Bandages", "Antibiotics"],
        "Stock": [120, 8, 45, 12]
    })
    fig = px.bar(items_df, x="Stock", y="Item", orientation='h', 
                 color="Stock", color_continuous_scale="Blues",
                 template="plotly_dark", height=200)
    fig.update_layout(showlegend=False, margin=dict(l=0, r=0, t=0, b=0))
    st.plotly_chart(fig, use_container_width=True)

    if st.button("🗑️ CLEAR SESSION", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# --- 6. MAIN INTERFACE ---
# Modern Header
st.markdown(f"""
    <div class='header-container'>
        <div>
            <h1 class='main-header'>GEMMA•PULSE</h1>
            <p style='color: #94a3b8; margin:0;'>Active Patient: <b>{p_id}</b> | {datetime.now().strftime('%H:%M')} Local</p>
        </div>
        <div style='text-align: right;'>
            <span style='background: rgba(16, 185, 129, 0.1); color: #10b981; padding: 5px 12px; border-radius: 20px; font-size: 0.8rem; border: 1px solid #10b981;'>
                ● LOCAL ENGINE ACTIVE
            </span>
        </div>
    </div>
""", unsafe_allow_html=True)

# Chat Display
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 7. INPUT SYSTEM (TEXT + VOICE) ---
input_col, voice_col = st.columns([0.85, 0.15])

with voice_col:
    # Voice Input Component
    audio = mic_recorder(start_prompt="🎤", stop_prompt="⏹️", key="recorder")

with input_col:
    prompt = st.chat_input("Enter symptoms, lab values, or triage data...")

# Logic for Audio Input
if audio:
    # Note: In a production environment, you'd send 'audio['bytes']' 
    # to a Whisper API or local STT model. 
    # Here we show the placeholder for the transcript.
    prompt = "Transcribing audio... [Voice Input Detected]"

# Process Input
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("Analyzing Clinical Data..."):
            res = engine.process_input(
                text_input=prompt, 
                history=st.session_state.messages[:-1],
                patient_context=context_str
            )
            st.markdown(res)
            st.session_state.messages.append({"role": "assistant", "content": res})

# Floating Export Action
if len(st.session_state.messages) > 0:
    st.download_button(
        label="📥 EXPORT CLINICAL REPORT",
        data=json.dumps(st.session_state.messages, indent=2),
        file_name=f"report_{p_id}.json",
        mime="application/json"
    )
