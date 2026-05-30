import streamlit as st
from src.yt_dload import (
    is_valid_syntax,
    is_link_live,
    get_transcrpt
)
from src.agent import get_summary_gemini, get_notes_gemini
from src.audio_gen import get_sum_tts
from src.ui_components import render_interactive_audio_agent


# -------------------------
# Page Config
# -------------------------

st.set_page_config(
    page_title="EchoAgent",
    page_icon="🎧",
    layout="centered"
)

st.title("EchoAgent")
st.caption("Transform YouTube Content into Insights")


# -------------------------
# Session State
# -------------------------

if "output" not in st.session_state:
    st.session_state.output = None

if "output_type" not in st.session_state:
    st.session_state.output_type = "Audio Summary"

if "audio_bytes" not in st.session_state:
    st.session_state.audio_bytes = None

if "show_agent_overlay" not in st.session_state:
    st.session_state.show_agent_overlay = False

if "video_link" not in st.session_state:
    st.session_state.video_link = ""


# -------------------------
# Input
# -------------------------

col1, col2 = st.columns([2, 1])

with col1:
    link = st.text_input(
        "Enter YouTube Link",
        key="video_link",
        placeholder="https://www.youtube.com/watch?v=..."
    )

with col2:
    output_choice = st.selectbox(
        "Choose Output Type",
        options=["Audio Summary", "Structured Notes (.md)"],
        key="selected_type"
    )


# -------------------------
# Generate
# -------------------------

if st.button(
    "Generate",
    use_container_width=True
):

    if not link:
        st.warning("Please enter a YouTube link.")
    elif not is_valid_syntax(link):
        st.error("Invalid YouTube link.")
    elif not is_link_live(link):
        st.warning("Video unavailable / private / deleted.")
    else:
        with st.spinner(f"Processing video for {output_choice}..."):
            try:
                transcript = get_transcrpt(link)

                if output_choice == "Audio Summary":
                    content = get_summary_gemini(transcript)
                    st.session_state.output = content
                    st.session_state.output_type = output_choice
                    
                    # Automate Audio Generation immediately
                    with st.spinner("Preparing AI Agent Narration..."):
                        st.session_state.audio_bytes = get_sum_tts(content)
                        st.session_state.show_agent_overlay = True
                else:
                    content = get_notes_gemini(transcript)
                    st.session_state.output = content
                    st.session_state.output_type = output_choice
                    st.session_state.audio_bytes = None
                    st.session_state.show_agent_overlay = False

                st.success("Success!")
            except Exception as e:
                st.error(f"Error: {e}")


# -------------------------
# Output Section
# -------------------------

if st.session_state.output:

    if st.session_state.output_type == "Structured Notes (.md)":
        st.divider()
        st.subheader("Notes")
        st.markdown(st.session_state.output)
        
        if st.button("Process Another Video", use_container_width=True):
            st.session_state.output = None
            st.session_state.video_link = ""
            st.rerun()
    
    elif st.session_state.output_type == "Audio Summary" and st.session_state.audio_bytes:
        # The interactive component handles the overlay
        # We also provide a way to re-open it or clear it
        st.divider()
        if st.button("Re-open AI Agent", use_container_width=True):
            st.session_state.show_agent_overlay = True
            st.rerun()

        if st.session_state.show_agent_overlay:
            # This renders the full-screen overlay
            render_interactive_audio_agent(st.session_state.output, st.session_state.audio_bytes)
            
            # Invisible or small button to help reset state if needed
            if st.button("✖ Exit Agent Mode", type="primary"):
                st.session_state.show_agent_overlay = False
                st.rerun()

        if st.button("Process Another Video", use_container_width=True):
            st.session_state.output = None
            st.session_state.audio_bytes = None
            st.session_state.show_agent_overlay = False
            st.session_state.video_link = ""
            st.rerun()
