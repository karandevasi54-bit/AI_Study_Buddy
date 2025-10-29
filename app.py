import os
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
from utils import extract_text_from_pdf, chunk_text
from prompts import SUMMARY_PROMPT, MCQ_PROMPT
from PyPDF2 import PdfReader

# Load environment variables
load_dotenv()

# Get OpenAI API key (works for both local + Streamlit Cloud)
api_key = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY")

if not api_key:
    st.error("⚠️ OpenAI API key not found. Please set it in .env or Streamlit Secrets.")
    st.stop()

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

# Streamlit page setup
st.set_page_config(page_title="AI Study Buddy — Summarize & Quiz", layout="wide")
st.title("📚 AI Study Buddy — Summarize & Quiz")
st.write("Upload notes or paste text to get instant summaries and quizzes.")

# File or text input
uploaded_file = st.file_uploader("Upload PDF or TXT:", type=["pdf", "txt"])
text = st.text_area("Or paste your notes here:", height=200)

# Extract text from uploaded PDF
if uploaded_file and not text:
    reader = PdfReader(uploaded_file)
    text = "\n".join(page.extract_text() or "" for page in reader.pages)

# Stop if no text provided
if not text:
    st.stop()

st.success(f"{len(text)} characters loaded successfully.")
nq = st.number_input("How many MCQs?", 3, 20, 5)
temp = st.slider("Creativity (temperature)", 0.0, 1.0, 0.1)

# Chat helper (new OpenAI API)
def chat(messages):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            max_tokens=900,
            temperature=temp,
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Error: {e}")
        return None

# --- Summarize Section ---
if st.button("📝 Summarize"):
    msgs = [
        {"role": "system", "content": "Summarize notes clearly for students."},
        {"role": "user", "content": SUMMARY_PROMPT.format(content=text)},
    ]
    output = chat(msgs)
    if output:
        st.subheader("🧩 Summary:")
        st.write(output)

# --- MCQ Generator Section ---
if st.button("❓ Generate MCQs"):
    msgs = [
        {"role": "system", "content": "Create helpful exam MCQs."},
        {"role": "user", "content": MCQ_PROMPT.format(content=text, n=nq)},
    ]
    output = chat(msgs)
    if output:
        st.subheader("🧠 Practice Questions:")
        st.write(output)
