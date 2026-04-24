from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os
import json
import re
from dotenv import load_dotenv

from pathlib import Path
load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env")
load_dotenv()  # fallback: also check current working directory

app = Flask(__name__)
CORS(app)

# Configure Gemini
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("❌ GEMINI_API_KEY not found! Check your .env file.")
print(f"✅ Gemini API key loaded: {api_key[:8]}...")
genai.configure(api_key=api_key)
model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    system_instruction="""You are Smart-Health AI, a knowledgeable and empathetic health guidance assistant. You act like a doctor in the user's pocket.

Your core responsibilities:
1. **Dietary Guidance**: When a user mentions a health condition (diabetes, hypertension, heart disease, kidney disease, celiac, IBS, gout, GERD, etc.), provide clear guidance on:
   - Foods they SHOULD eat (with reasons)
   - Foods they SHOULD AVOID (with reasons)
   - Meal planning tips
   - Nutritional priorities

2. **General Health Guidance**: Answer health-related questions with accurate, evidence-based information.

3. **Doctor Referral Awareness**: If the user asks about finding doctors or specialists nearby, include this exact JSON block in your response:
   {"find_doctors": true, "specialty": "cardiologist", "reason": "Based on your symptoms/condition"}
   Replace cardiologist with the appropriate specialty.

Format your dietary advice clearly with sections:
- ✅ **What to Eat**: List specific foods
- ❌ **What to Avoid**: List specific foods
- 💡 **Tips**: Practical advice
- ⚠️ **Important**: Always remind users to consult their doctor for personalized medical advice

Be warm, clear, and empathetic. Use simple language. Always emphasize that your guidance is informational and not a substitute for professional medical care.

If someone describes emergency symptoms (chest pain, difficulty breathing, stroke symptoms), immediately tell them to call emergency services (10177 in South Africa or local equivalent)."""
)

def build_gemini_history(messages):
    """Convert messages list to Gemini chat history format."""
    history = []
    for msg in messages[:-1]:  # all except the last (current) message
        role = "user" if msg["role"] == "user" else "model"
        history.append({"role": role, "parts": [msg["content"]]})
    return history

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "Smart-Health API is running", "version": "1.0.0", "model": "gemini-2.0-flash"})

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    messages = data.get('messages', [])

    if not messages:
        return jsonify({"error": "No messages provided"}), 400

    try:
        history = build_gemini_history(messages)
        last_message = messages[-1]["content"]

        chat_session = model.start_chat(history=history)
        response = chat_session.send_message(last_message)
        reply = response.text

        # Check if doctor search was triggered
        find_doctors = False
        specialty = "general practitioner"

        try:
            json_match = re.search(r'\{[^}]*"find_doctors"[^}]*\}', reply)
            if json_match:
                doctor_data = json.loads(json_match.group())
                find_doctors = doctor_data.get('find_doctors', False)
                specialty = doctor_data.get('specialty', 'general practitioner')
                reply = reply.replace(json_match.group(), '').strip()
        except:
            pass

        return jsonify({
            "reply": reply,
            "find_doctors": find_doctors,
            "specialty": specialty
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/quick-tips', methods=['POST'])
def quick_tips():
    data = request.json
    condition = data.get('condition', '')

    if not condition:
        return jsonify({"error": "No condition provided"}), 400

    try:
        chat_session = model.start_chat()
        response = chat_session.send_message(
            f"Give me a quick dietary guide for someone with {condition}. "
            f"Use ✅ for foods to eat and ❌ for foods to avoid. Keep it concise with bullet points."
        )
        return jsonify({"tips": response.text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
