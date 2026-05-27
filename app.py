import streamlit as st
from src.yt_dload import is_valid_syntax, is_link_live, get_transcrpt
from src.agent import get_summary_gemini
from src.audio_gen import get_sum_tts

st.title("EchoAgent")
st.subheader("Save-Time Save-Effort")

# Initialize session state
if "summary" not in st.session_state:
    st.session_state.summary = None

link = st.text_input("Enter your Youtube Video Link")

if st.button("Submit"):
    if is_valid_syntax(link):
        if is_link_live(link):
            st.success("Link is Valid and processing will start soon")

            transcript = get_transcrpt(link)
            summary = get_summary_gemini(transcript)

            # Store summary
            st.session_state.summary = summary

            st.success("Summary Generated!")

        else:
            st.warning("Video is unavailable / private / deleted")
    else:
        st.error("Invalid link")

# 👇 This runs independently
if st.session_state.summary:
    st.write("### Summary:")
    st.write(st.session_state.summary)

    if st.button("Generate and Play Audio"):
        with st.spinner("Generating audio..."):
            try:
                audio_bytes = get_sum_tts(st.session_state.summary)
                st.audio(audio_bytes, format="audio/wav")
                st.success("Audio ready!")
            except Exception as e:
                st.error(f"Error: {e}")