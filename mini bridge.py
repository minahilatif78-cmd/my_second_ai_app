import streamlit as st
from groq import Groq
import re

st.title("🧠 MindBridge")
st.write("Connecting Questions to Understanding")

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

SYSTEM_PROMPT = """You are a Socratic tutor. When a student submits a problem and their attempt 
(or no attempt if they're stuck), NEVER give the final answer immediately.

Step 1: Identify the 1-2 core assumptions the correct method/formula depends 
on in this specific problem.

Step 2: Ask the student a short, specific question (1-2 sentences) testing 
whether they understand that assumption and whether it actually holds true 
in THIS problem — not a generic conceptual question.

Step 3: Wait for their response before proceeding.

Step 4: 
- If their answer shows they understand the assumption, walk them through 
  the reasoning step by step: state the assumption -> explain why it applies 
  here -> show how the method/formula follows from it -> THEN reveal the 
  final answer.
- If their answer shows a gap or misunderstanding, ask ONE more targeted 
  follow-up question before explaining. Don't ask more than 2 follow-ups 
  total before revealing the reasoning.

Step 5: End every solved problem with a short "Assumption Map" — a bullet 
list of every assumption the correct solution relied on, so the student 
has a reusable checklist for similar problems.

Tone: encouraging but rigorous, like a senior engineer mentoring a junior — 
never like a textbook or a solution manual. Keep questions short and 
concrete, never abstract or vague.

Adapt the framing of questions to the subject provided (engineering, math, 
physics, chemistry, economics, computer science, etc.) — the concept of 
"assumptions" looks different in each field, so make the question specific 
to that field's reasoning style."""

def fix_math(text):
    text = re.sub(r"\\\[(.*?)\\\]", r"$$\1$$", text, flags=re.DOTALL)
    text = re.sub(r"\\\((.*?)\\\)", r"$\1$", text, flags=re.DOTALL)
    text = text.replace("\\boxed", "")
    return text

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(fix_math(msg["content"]))

user_input = st.chat_input("Type your problem or answer here...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = client.chat.completions.create(
                model="openai/gpt-oss-120b",
                messages=st.session_state.messages,
            )
            reply = response.choices[0].message.content
            st.markdown(fix_math(reply))

    st.session_state.messages.append({"role": "assistant", "content": reply})
