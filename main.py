# main.py

import streamlit as st
from agent import root_agent
import tempfile

st.set_page_config(page_title="CV Analyzer", page_icon="📄")
st.title("📄 CV Analyzer - Find the Best Jobs for You")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# File upload
uploaded_file = st.file_uploader("📤 Upload your CV (PDF, DOCX, or TXT)", type=["pdf", "docx", "txt"])

# User input if no file
if not uploaded_file:
    job_role = st.text_input("🔍 Desired Job Role")
    location = st.text_input("📍 Preferred Location")
    experience = st.text_input("💼 Years of Experience")
    salary = st.text_input("💰 Salary Expectation (Optional)")

    if st.button("Find Jobs"):
        prompt = f"""I am looking for a job.
        Role: {job_role}
        Location: {location}
        Experience: {experience}
        Salary Expectation: {salary or "Not specified"}
        """
        response = root_agent.chat(prompt)
        st.session_state.chat_history.append(("user", prompt))
        st.session_state.chat_history.append(("agent", response.text))
else:
    # Save uploaded file to a temporary location
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(uploaded_file.read())
        file_path = tmp.name

    st.success("✅ CV uploaded! Extracting information and searching jobs...")

    with st.spinner("Processing..."):
        # You can enhance this to use parse_cv_with_gemini or add your own logic
        response = root_agent.chat(f"Please analyze this resume: {file_path}")
        st.session_state.chat_history.append(("user", "Uploaded a resume"))
        st.session_state.chat_history.append(("agent", response.text))

# Chat history display
for speaker, message in st.session_state.chat_history:
    if speaker == "user":
        st.markdown(f"🧑 **You**: {message}")
    else:
        st.markdown(f"🤖 **Agent**: {message}")


    with st.spinner("Processing..."):
        # You can enhance this to use parse_cv_with_gemini or add your own logic
        response = root_agent.chat(f"Please analyze this resume: {file_path}")
        st.session_state.chat_history.append(("user", "Uploaded a resume"))
        st.session_state.chat_history.append(("agent", response.text))

# Chat history display
for speaker, message in st.session_state.chat_history:
    if speaker == "user":
        st.markdown(f"🧑 **You**: {message}")
    else:
        st.markdown(f"🤖 **Agent**: {message}")
