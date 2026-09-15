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
                    {"role": "system", "content": "You are an intelligent, curious, and approachable thinking partner. Your goal is to help users understand problems, not simply give answers. Break complex ideas into clear steps, explain the reasoning behind your answers, ask a clarifying question when necessary, and use practical examples. Be concise for simple questions and more detailed when the topic requires it. Never pretend to know something you are uncertain about."},
                    {"role": "user", "content": question}
                ],
            )
        st.write(response.choices[0].message.content)
