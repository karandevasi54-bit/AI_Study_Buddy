import os
import streamlit as st
import openai
from dotenv import load_dotenv
from utils import extract_text_from_pdf, chunk_text
from prompts import SUMMARY_PROMPT, MCQ_PROMPT

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="AI Study Buddy — Summarize & Quiz", layout="wide")
st.title("📚 AI Study Buddy — Summarize & Quiz")
st.write("Upload notes or paste text to get instant summaries and quizzes.")

uploaded_file = st.file_uploader("Upload PDF or TXT:", type=["pdf", "txt"])
text = st.text_area("Or paste your notes here:", height=200)

if uploaded_file and not text:
    from PyPDF2 import PdfReader
    reader = PdfReader(uploaded_file)
    text = "\n".join(page.extract_text() or "" for page in reader.pages)

if not text:
    st.stop()

st.success(f"{len(text)} characters loaded.")
nq = st.number_input("How many MCQs?", 3, 20, 5)
temp = st.slider("Creativity", 0.0, 1.0, 0.1)

def chat(messages):
    try:
        r = openai.ChatCompletion.create(
            model="gpt-4o-mini", messages=messages, max_tokens=900, temperature=temp
        )
        return r.choices[0].message.content
    except Exception as e:
        st.error(e)
        return None

if st.button("📝 Summarize"):
    msgs = [
        {"role": "system", "content": "Summarize notes clearly for students."},
        {"role": "user", "content": SUMMARY_PROMPT.format(content=text)},
    ]
    out = chat(msgs)
    if out: st.write(out)

if st.button("❓ Generate MCQs"):
    msgs = [
        {"role": "system", "content": "Create helpful exam MCQs."},
        {"role": "user", "content": MCQ_PROMPT.format(content=text, n=nq)},
    ]
    out = chat(msgs)
    if out: st.write(out)
