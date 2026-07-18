import streamlit as st
import requests
import json

def generate_with_fallback(prompt):
    # Grab the key directly from secrets
    api_key = st.secrets["GEMINI_API_KEY"].strip().replace('"', '').replace("'", "")
    
    # Standard, direct Google AI Studio endpoint (explicitly using v1beta)
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    
    headers = {
        "Content-Type": "application/json"
    }
    
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }
    
    # Direct network request bypasses all SDK environment variables completely
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    response_json = response.json()
    
    if response.status_code == 200:
        return response_json["candidates"][0]["content"]["parts"][0]["text"]
    else:
        error_msg = response_json.get("error", {}).get("message", f"HTTP {response.status_code}")
        raise Exception(error_msg)