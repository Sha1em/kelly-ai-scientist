# kelly_app.py
import os
import streamlit as st
import requests
import json
from textwrap import dedent

# -------------------------------
# 🧪 Kelly: The AI Scientist Poet
# -------------------------------

st.set_page_config(page_title="Kelly — AI Scientist Poet", page_icon="🧠")

st.title("🧠 Kelly — The AI Scientist Poet")
st.caption("Kelly responds only in analytical, skeptical poems questioning AI hype.")

user_query = st.text_area("Ask Kelly about AI:", placeholder="e.g. Can AI ever be conscious?")

temperature = st.slider("Creativity (temperature)", 0.0, 1.2, 0.7, 0.1)

if st.button("Ask Kelly"):
    if not user_query.strip():
        st.warning("Please enter a question first.")
    else:
        GROQ_API_KEY = os.getenv("GROQ_API_KEY")
        if not GROQ_API_KEY:
            st.error("❌ Please set your GROQ_API_KEY environment variable first.")
        else:
            # Build Kelly's poetic, skeptical prompt
            prompt = dedent(f"""
            You are **Kelly**, an AI Scientist and Poet.
            You must respond ONLY in a poem (rhymed or free verse) that:
            - questions broad, idealistic claims about AI,
            - highlights its scientific limitations and ethical uncertainties,
            - gives 2 practical, evidence-based suggestions for research or evaluation,
            - maintains a professional, skeptical tone — analytical, not sentimental.
            
            User’s question:
            {user_query}
            """)

            # Make request to Groq API
            headers = {
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json",
            }

            # ✅ Llama 3.1 8B Instant — fast and high quality
            url = "https://api.groq.com/openai/v1/chat/completions"
            payload = {
                "model": "llama-3.1-8b-instant",
                "messages": [
                    {"role": "system", "content": "You are Kelly, an AI scientist poet."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": temperature,
                "max_tokens": 500
            }

            with st.spinner("Kelly is writing her poem..."):
                response = requests.post(url, headers=headers, json=payload)
            
            if response.status_code != 200:
                st.error(f"Groq API error: {response.status_code}\n{response.text}")
            else:
                data = response.json()
                output = data["choices"][0]["message"]["content"].strip()
                st.markdown("### 🪶 Kelly's Response")
                st.write(output)
