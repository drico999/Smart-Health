# 🩺 Smart-Health — AI Health Guidance & Doctor Finder

Smart-Health is a full-stack AI-powered health companion that provides:
- 🥗 Dietary guidance for specific health conditions
- 💬 Conversational health Q&A (like a doctor in your pocket)
- 🗺️ Doctor/specialist finder (via Google Maps integration)
- ⚡ Quick condition guides for 12 common conditions

---

## 🏗️ Architecture

```
smart-health/
├── backend/
│   ├── app.py            ← Flask API (port 5000)
│   └── requirements.txt
└── frontend/
    ├── app.py            ← Streamlit UI (port 8501)
    └── requirements.txt
```

---

## 🚀 Setup & Running

### 1. Prerequisites
- Python 3.9+
- An Anthropic API key → https://console.anthropic.com

### 2. Backend (Flask)

```bash
cd backend
pip install -r requirements.txt

# Set your Anthropic API key
export ANTHROPIC_API_KEY="sk-ant-..."   # Mac/Linux
set ANTHROPIC_API_KEY=sk-ant-...        # Windows CMD

python app.py
```
Flask will start on → **http://localhost:5000**

### 3. Frontend (Streamlit)

Open a **new terminal**:

```bash
cd frontend
pip install -r requirements.txt
streamlit run app.py
```
Streamlit will open → **http://localhost:8501**

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| POST | `/chat` | Main chat endpoint |
| POST | `/quick-tips` | Quick condition dietary tips |

### POST `/chat`
```json
{
  "messages": [
    {"role": "user", "content": "What should I eat if I have diabetes?"}
  ]
}
```
**Response:**
```json
{
  "reply": "Here's your dietary guide for diabetes...",
  "find_doctors": false,
  "specialty": null
}
```

### POST `/quick-tips`
```json
{ "condition": "hypertension" }
```

---

## 💡 Features

### Health Guidance
Ask about any condition and get:
- ✅ Foods to eat
- ❌ Foods to avoid
- 💡 Practical tips
- ⚠️ When to see a doctor

### Doctor Finder
Phrases like *"find me a cardiologist"* or *"I need a specialist near me"* will trigger the Google Maps integration, filtered by your location (set in the sidebar).

### Quick Condition Guides
One-click dietary summaries for:
Diabetes · Hypertension · Heart Disease · High Cholesterol · Kidney Disease · Gout · GERD · Celiac · IBS · Fatty Liver · Anaemia · Hypothyroid

---

## ⚠️ Disclaimer
Smart-Health provides **informational guidance only** and is not a substitute for professional medical advice. Always consult a qualified healthcare provider for diagnosis and treatment.