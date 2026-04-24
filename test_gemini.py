from dotenv import load_dotenv
import os
load_dotenv()

key = os.getenv("GEMINI_API_KEY")
print("KEY:", key[:10] if key else "NOT FOUND")

import google.generativeai as genai
genai.configure(api_key=key)

model = genai.GenerativeModel('gemini-2.0-flash')
chat = model.start_chat()
response = chat.send_message('say hello')
print("SUCCESS:", response.text[:100])