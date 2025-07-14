from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
import cohere
import os
import re

app = FastAPI()

# --- CORS (so the extension can access the API) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"]
)

# --- Initialize Cohere with your real API key ---
co = cohere.Client("ERoJiNHuDiaw5pNvLQOQvxniFYsdxI5M7rMLVj0d")

# --- Function to clean markdown-style output ---
def clean_json_output(text):
    # Removes markdown code block formatting like ```json\n...\n```
    return re.sub(r"```(?:json)?\s*(.*?)\s*```", r"\1", text.strip(), flags=re.DOTALL)

# --- Threat Detection Endpoint ---
@app.post("/analyze")
def analyze_threat(message: str = Form(...)):
    prompt = f"""
You are an AI assistant trained to detect threats, scams, phishing, manipulation, and psychological abuse in user messages.

Analyze the message and return a JSON object with:
- risk_level: (Safe / Caution / Dangerous)
- red_flags: List
- tone: (e.g., manipulative, urgent)
- suggestion: A safe response
- confidence: 0 to 100

Message:
\"\"\"{message}\"\"\"

Respond only in JSON format.
"""
    try:
        response = co.generate(
            model="command-r-plus",
            prompt=prompt,
            max_tokens=300,
            temperature=0.4
        )
        raw_output = response.generations[0].text
        cleaned_output = clean_json_output(raw_output)
        return {"result": cleaned_output}
    except Exception as e:
        return {"error": str(e)}
