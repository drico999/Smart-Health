
import streamlit as st
import requests
import json
import urllib.parse

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Smart-Health",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

BACKEND_URL = "http://localhost:5000"

# ── Custom CSS ──────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;1,9..40,300&display=swap');

  /* ── Global ── */
  html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
  }

  .stApp {
    background: linear-gradient(135deg, #0a1628 0%, #0d2137 40%, #0a2820 100%);
    min-height: 100vh;
  }

  /* ── Header ── */
  .sh-header {
    background: linear-gradient(90deg, rgba(0,200,150,0.12) 0%, rgba(0,150,255,0.08) 100%);
    border: 1px solid rgba(0,200,150,0.25);
    border-radius: 20px;
    padding: 28px 36px;
    margin-bottom: 28px;
    backdrop-filter: blur(10px);
    display: flex;
    align-items: center;
    gap: 18px;
  }
  .sh-logo {
    font-size: 2.8rem;
  }
  .sh-title {
    font-family: 'DM Serif Display', serif;
    font-size: 2.4rem;
    color: #00e6a0;
    margin: 0;
    line-height: 1.1;
    letter-spacing: -0.5px;
  }
  .sh-subtitle {
    color: rgba(180,220,210,0.75);
    font-size: 0.95rem;
    margin: 4px 0 0;
    font-weight: 300;
    letter-spacing: 0.3px;
  }

  /* ── Chat messages ── */
  .msg-wrap { margin-bottom: 18px; animation: fadeUp 0.35s ease; }
  @keyframes fadeUp {
    from { opacity:0; transform:translateY(10px); }
    to   { opacity:1; transform:translateY(0); }
  }

  .msg-user {
    background: linear-gradient(135deg, #0066cc, #004499);
    border: 1px solid rgba(0,120,255,0.4);
    border-radius: 18px 18px 4px 18px;
    padding: 14px 18px;
    margin-left: 15%;
    color: #e8f4ff;
    font-size: 0.95rem;
    line-height: 1.6;
    box-shadow: 0 4px 20px rgba(0,100,220,0.25);
  }

  .msg-assistant {
    background: linear-gradient(135deg, rgba(0,40,30,0.9), rgba(0,30,25,0.95));
    border: 1px solid rgba(0,200,150,0.25);
    border-radius: 18px 18px 18px 4px;
    padding: 16px 20px;
    margin-right: 10%;
    color: #d0f0e8;
    font-size: 0.94rem;
    line-height: 1.7;
    box-shadow: 0 4px 24px rgba(0,180,120,0.12);
  }

  .msg-label {
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 1.2px;
    text-transform: uppercase;
    margin-bottom: 6px;
    opacity: 0.65;
  }
  .msg-user .msg-label { color: #7bb8ff; text-align: right; }
  .msg-assistant .msg-label { color: #00c896; }

  /* ── Doctor card ── */
  .doctor-card {
    background: linear-gradient(135deg, rgba(255,160,0,0.08), rgba(255,100,0,0.05));
    border: 1px solid rgba(255,160,0,0.3);
    border-radius: 16px;
    padding: 18px 22px;
    margin-top: 14px;
    color: #ffe0a0;
  }
  .doctor-card h4 {
    color: #ffb830;
    font-family: 'DM Serif Display', serif;
    font-size: 1.1rem;
    margin: 0 0 10px;
  }
  .doctor-link {
    display: inline-block;
    background: linear-gradient(90deg, #ffb830, #ff8c00);
    color: #1a0a00 !important;
    padding: 8px 18px;
    border-radius: 30px;
    font-weight: 600;
    font-size: 0.85rem;
    text-decoration: none !important;
    margin-top: 10px;
    transition: all 0.2s;
    letter-spacing: 0.3px;
  }

  /* ── Sidebar ── */
  [data-testid="stSidebar"] {
    background: linear-gradient(180deg, #061020 0%, #071a12 100%) !important;
    border-right: 1px solid rgba(0,200,150,0.15);
  }
  [data-testid="stSidebar"] * { color: #b0d8c8 !important; }

  .condition-chip {
    display: inline-block;
    background: rgba(0,200,150,0.12);
    border: 1px solid rgba(0,200,150,0.3);
    border-radius: 20px;
    padding: 5px 12px;
    font-size: 0.78rem;
    margin: 3px;
    cursor: pointer;
    color: #00d4a0 !important;
    transition: all 0.2s;
  }

  /* ── Input area ── */
  .stTextInput > div > div > input,
  .stChatInput textarea {
    background: rgba(0,30,20,0.8) !important;
    border: 1.5px solid rgba(0,200,150,0.3) !important;
    border-radius: 12px !important;
    color: #d0f0e8 !important;
    font-family: 'DM Sans', sans-serif !important;
  }
  .stChatInput textarea:focus {
    border-color: rgba(0,200,150,0.7) !important;
    box-shadow: 0 0 0 3px rgba(0,200,150,0.1) !important;
  }

  /* ── Buttons ── */
  .stButton > button {
    background: linear-gradient(135deg, #00a870, #007a50) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    transition: all 0.2s !important;
  }
  .stButton > button:hover {
    background: linear-gradient(135deg, #00c484, #009060) !important;
    transform: translateY(-1px);
    box-shadow: 0 4px 15px rgba(0,180,120,0.35) !important;
  }

  /* ── Quick tips box ── */
  .tips-box {
    background: rgba(0,20,15,0.7);
    border: 1px solid rgba(0,200,150,0.2);
    border-radius: 14px;
    padding: 16px 18px;
    margin-top: 12px;
    color: #c0e8d8;
    font-size: 0.88rem;
    line-height: 1.7;
    white-space: pre-wrap;
  }

  /* ── Emergency banner ── */
  .emergency-banner {
    background: linear-gradient(90deg, rgba(200,0,50,0.15), rgba(180,0,30,0.1));
    border: 1px solid rgba(220,50,80,0.5);
    border-radius: 12px;
    padding: 12px 18px;
    color: #ff8090;
    font-size: 0.85rem;
    margin-bottom: 18px;
  }

  /* Scrollbar */
  ::-webkit-scrollbar { width: 6px; }
  ::-webkit-scrollbar-track { background: rgba(0,20,15,0.4); }
  ::-webkit-scrollbar-thumb { background: rgba(0,200,150,0.3); border-radius: 3px; }

  /* Hide streamlit default chrome */
  #MainMenu, footer, header { visibility: hidden; }
  .block-container { padding-top: 1.5rem !important; padding-bottom: 1rem !important; }
</style>
""", unsafe_allow_html=True)

# ── Session state ──────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "quick_tips" not in st.session_state:
    st.session_state.quick_tips = None
if "user_location" not in st.session_state:
    st.session_state.user_location = ""

# ── Helper functions ───────────────────────────────────────────────────────────
def send_message(user_input):
    st.session_state.messages.append({"role": "user", "content": user_input})
    try:
        resp = requests.post(
            f"{BACKEND_URL}/chat",
            json={"messages": st.session_state.messages},
            timeout=30
        )
        if resp.status_code == 200:
            data = resp.json()
            st.session_state.messages.append({
                "role": "assistant",
                "content": data["reply"]
            })
            return data
        else:
            st.error("Backend error. Is the Flask server running?")
            return None
    except requests.exceptions.ConnectionError:
        st.error("⚠️ Cannot connect to Smart-Health backend. Please start the Flask server on port 5000.")
        st.session_state.messages.pop()
        return None

def get_quick_tips(condition):
    try:
        resp = requests.post(
            f"{BACKEND_URL}/quick-tips",
            json={"condition": condition},
            timeout=20
        )
        if resp.status_code == 200:
            return resp.json().get("tips", "")
    except:
        return None

def build_google_maps_url(specialty, location=None):
    query = f"{specialty} near me" if not location else f"{specialty} near {location}"
    encoded = urllib.parse.quote(query)
    return f"https://www.google.com/maps/search/{encoded}"

def render_message(msg):
    role = msg["role"]
    content = msg["content"]
    if role == "user":
        st.markdown(f"""
        <div class="msg-wrap">
          <div class="msg-user">
            <div class="msg-label">You</div>
            {content}
          </div>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="msg-wrap">
          <div class="msg-assistant">
            <div class="msg-label">🩺 Smart-Health AI</div>
            {content}
          </div>
        </div>""", unsafe_allow_html=True)

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🩺 Smart-Health")
    st.markdown("---")

    st.markdown("**📍 Your Location** *(for doctor search)*")
    location_input = st.text_input(
        "City or area",
        value=st.session_state.user_location,
        placeholder="e.g. Johannesburg, Sandton",
        label_visibility="collapsed"
    )
    if location_input != st.session_state.user_location:
        st.session_state.user_location = location_input

    st.markdown("---")
    st.markdown("**⚡ Quick Condition Guide**")
    st.markdown("Tap a condition for instant dietary tips:")

    conditions = [
        "Diabetes Type 2", "Hypertension", "Heart Disease",
        "High Cholesterol", "Kidney Disease", "Gout",
        "GERD / Acid Reflux", "Celiac Disease", "IBS",
        "Fatty Liver", "Anaemia", "Thyroid (Hypothyroid)"
    ]

    cols = st.columns(2)
    for i, cond in enumerate(conditions):
        with cols[i % 2]:
            if st.button(cond, key=f"cond_{i}", use_container_width=True):
                with st.spinner(f"Getting tips for {cond}..."):
                    tips = get_quick_tips(cond)
                    if tips:
                        st.session_state.quick_tips = {"condition": cond, "tips": tips}

    st.markdown("---")
    st.markdown("**🚨 Emergency?**")
    st.markdown(
        '<div class="emergency-banner">If you have chest pain, difficulty breathing, or signs of stroke — call <strong>10177</strong> (SA) or your local emergency number immediately.</div>',
        unsafe_allow_html=True
    )

    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.quick_tips = None
        st.rerun()

# ── Main layout ────────────────────────────────────────────────────────────────
st.markdown("""
<div class="sh-header">
  <div class="sh-logo">🩺</div>
  <div>
    <div class="sh-title">Smart-Health</div>
    <div class="sh-subtitle">Your AI health companion · dietary guidance · doctor finder</div>
  </div>
</div>
""", unsafe_allow_html=True)

# Quick tips panel
if st.session_state.quick_tips:
    qt = st.session_state.quick_tips
    with st.expander(f"📋 Quick Guide: {qt['condition']}", expanded=True):
        st.markdown(f'<div class="tips-box">{qt["tips"]}</div>', unsafe_allow_html=True)
        if st.button("Ask more about this condition →", key="ask_more"):
            send_message(f"Tell me more about managing {qt['condition']} — what lifestyle changes help and what should I watch out for?")
            st.session_state.quick_tips = None
            st.rerun()

# Chat history
chat_container = st.container()
with chat_container:
    if not st.session_state.messages:
        st.markdown("""
        <div style="text-align:center; padding: 50px 20px; color: rgba(160,210,190,0.5);">
          <div style="font-size:3rem; margin-bottom:16px;">💬</div>
          <div style="font-family:'DM Serif Display',serif; font-size:1.3rem; color:rgba(0,200,150,0.6);">
            How can I help you today?
          </div>
          <div style="font-size:0.88rem; margin-top:10px; max-width:400px; margin-inline:auto; line-height:1.7;">
            Ask me about what to eat for a condition, get health guidance, or find doctors near you.
          </div>
        </div>
        """, unsafe_allow_html=True)

        # Starter prompts
        st.markdown("<br>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        starters = [
            ("🥗", "What should I eat if I have diabetes?"),
            ("❤️", "Foods to avoid with high blood pressure"),
            ("👨‍⚕️", "Find me a cardiologist nearby"),
        ]
        for col, (icon, prompt) in zip([c1, c2, c3], starters):
            with col:
                if st.button(f"{icon} {prompt}", key=f"starter_{prompt[:15]}", use_container_width=True):
                    result = send_message(prompt)
                    st.rerun()
    else:
        for msg in st.session_state.messages:
            render_message(msg)

        # Doctor finder card (if triggered)
        last_response = None
        try:
            resp_check = requests.post(
                f"{BACKEND_URL}/chat",
                json={"messages": [{"role": "user", "content": "_ping_"}]},
                timeout=2
            )
        except:
            pass

# ── Chat input ─────────────────────────────────────────────────────────────────
user_input = st.chat_input("Ask about a condition, diet, symptoms, or find doctors...")

if user_input:
    result = send_message(user_input)
    if result:
        if result.get("find_doctors"):
            specialty = result.get("specialty", "general practitioner")
            location = st.session_state.user_location or "near me"
            maps_url = build_google_maps_url(specialty, location)
            st.markdown(f"""
            <div class="doctor-card">
              <h4>🗺️ Find a {specialty.title()} Near You</h4>
              <div>Based on your query, we recommend consulting a <strong>{specialty}</strong>.</div>
              <a class="doctor-link" href="{maps_url}" target="_blank">
                📍 Search on Google Maps →
              </a>
            </div>
            """, unsafe_allow_html=True)
    st.rerun()

