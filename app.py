from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
import cohere
import os

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"]
)

co = cohere.Client("ERoJiNHuDiaw5pNvLQOQvxniFYsdxI5M7rMLVj0d")  # Your API key

@app.post("/analyze")
def analyze_threat(message: str = Form(...)):
    prompt = f"""
You are an AI assistant trained to detect threats.

Message:
\"\"\"{message}\"\"\"

Return a JSON object with:
- risk_level
- red_flags
- tone
- suggestion
- confidence
"""
    response = co.generate(model="command-r-plus", prompt=prompt, max_tokens=300, temperature=0.4)
    return {"result": response.generations[0].text.strip()}
