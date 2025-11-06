import os
import streamlit as st
import requests
import json
from textwrap import dedent

# -------------------------------
# 🧪 Kelly: The AI Scientist Poet
# -------------------------------

st.set_page_config(
    page_title="Kelly — AI Scientist Poet",
    page_icon="🧠",
    layout="centered",
)

# Custom CSS styling
st.markdown(
    """
    <style>
    body {
        background: linear-gradient(135deg, #0f172a, #1e293b);
        color: #e2e8f0;
    }
    .main {
        background-color: rgba(255,255,255,0.05);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 0 20px rgba(0,0,0,0.3);
    }
    h1 {
        color: #38bdf8 !important;
        text-align: center;
        font-family: 'Georgia', serif;
        font-size: 2.4rem;
    }
    h3, .stMarkdown, label, .stTextArea, .stSlider {
        font-family: 'Cambria', serif !important;
    }
    .stButton button {
        background: linear-gradient(90deg, #2563eb, #0ea5e9);
        color: white;
        border-radius: 10px;
        border: none;
        padding: 0.6rem 1.2rem;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton button:hover {
        background: linear-gradient(90deg, #0ea5e9, #2563eb);
        transform: scale(1.05);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Title section
st.title("🧠 Kelly — The AI Scientist Poet")
st.markdown(
    "<p style='text-align:center;color:#94a3b8;'>"
    "Kelly answers only in poetic reflections on AI — skeptical, analytical, and evidence-driven."
    "</p>",
    unsafe_allow_html=True,
)

st.divider()

# Input area
st.subheader("💭 Pose your question to Kelly")
user_query = st.text_area(
    "",
    placeholder="e.g. Can AI ever be conscious?",
    height=120,
)

st.markdown("<br>", unsafe_allow_html=True)

# Temperature slider with label
st.markdown("🎨 **Creativity (temperature)**")
temperature = st.slider("", 0.0, 1.2, 0.7, 0.1)

st.markdown("<br>", unsafe_allow_html=True)

# Action button
if st.button("✍️ Ask Kelly"):
    if not user_query.strip():
        st.warning("⚠️ Please enter a question first.")
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

            with st.spinner("✒️ Kelly is composing her scientific verse..."):
                response = requests.post(url, headers=headers, json=payload)
            
            if response.status_code != 200:
                st.error(f"Groq API error: {response.status_code}\n{response.text}")
            else:
                data = response.json()
                output = data["choices"][0]["message"]["content"].strip()
                st.markdown("---")
                st.markdown("### 🪶 Kelly’s Response")
                st.markdown(
                    f"<div style='background-color:#1e293b;padding:1.5rem;border-radius:15px;color:#f1f5f9;'>"
                    f"{output}</div>",
                    unsafe_allow_html=True,
                )
