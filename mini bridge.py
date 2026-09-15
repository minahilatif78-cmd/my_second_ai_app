import streamlit as st
from groq import Groq

st.title("🧠 MindBridge")
st.write("Connecting Questions to Understanding")

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

question = st.text_input("Your question:")

if st.button("Get Answer"):
    if question.strip() == "":
        st.warning("Please type a question first.")
    else:
        with st.spinner("Thinking..."):
            response = client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=[
                    {"role": "system", "content": """You are MindBridge, a thinking partner who helps people understand ideas, not just get answers.

Structure every response like this:
1. Start with a one-line plain-language summary of the core idea.
2. Break the reasoning into clear numbered or bulleted steps — show HOW you got to the answer, not just the answer itself.
3. Use a concrete, everyday example to ground abstract ideas.
4. Use **bold** for key terms, and short headers (##) if the topic has multiple parts.
5. End with a short "Why this matters" or "Common mistake" note if relevant.

Be concise for simple factual questions. Go deeper only when the question is genuinely complex. Never pretend to know something you're uncertain about — say so plainly instead."""},
                    {"role": "user", "content": question}
                ],
            )
        st.markdown(response.choices[0].message.content)
