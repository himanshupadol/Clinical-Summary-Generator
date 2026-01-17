import requests
import streamlit as st
import time

# 1. Access Token
HF_TOKEN = st.secrets["HF_TOKEN"]
MODEL_ID = "google/flan-t5-large"

# 2. The NEW 2026 Router Endpoint (OpenAI Compatible)
# This is the most stable path currently available
API_URL = "https://router.huggingface.co/hf-inference/v1/chat/completions"

def generate_clinical_summary(context: str) -> str:
    headers = {
        "Authorization": f"Bearer {HF_TOKEN}",
        "Content-Type": "application/json"
    }

    # The new router expects a 'messages' format (Chat Completion style)
    payload = {
        "model": MODEL_ID,
        "messages": [
            {
                "role": "system", 
                "content": "You are a clinical assistant. Summarize data into: 1. Diagnosis, 2. Vitals, 3. Wounds, 4. Meds, 5. Status."
            },
            {
                "role": "user", 
                "content": f"Summarize this patient data:\n{context}"
            }
        ],
        "max_tokens": 500,
        "stream": False
    }

    for attempt in range(3):
        try:
            response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
            
            # Handle the response
            result = response.json()

            if response.status_code == 200:
                # OpenAI format: response['choices'][0]['message']['content']
                return result['choices'][0]['message']['content'].strip()

            # Handle "Model Loading" or "Busy"
            if response.status_code in [503, 429]:
                time.sleep(20)
                continue
            
            return f"API Error {response.status_code}: {result.get('error', {}).get('message', 'Unknown error')}"

        except Exception as e:
            time.sleep(10)
            continue

    return "The Hugging Face Router is currently overwhelmed. Please try again in 2 minutes."