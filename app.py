import streamlit as st
from src.yt_dload import (
    is_valid_syntax,
    is_link_live,
    get_transcrpt
)
from src.agent import get_summary_gemini
from src.audio_gen import get_sum_tts


# -------------------------
# Page Config
# -------------------------

st.set_page_config(
    page_title="EchoAgent",
    page_icon="🎧",
    layout="centered"
)

st.title("EchoAgent")
st.caption("Save Time • Save Effort")


# -------------------------
# Session State
# -------------------------

if "summary" not in st.session_state:
    st.session_state.summary = None

if "video_link" not in st.session_state:
    st.session_state.video_link = ""


# -------------------------
# Input
# -------------------------

link = st.text_input(
    "Enter your YouTube Video Link",
    key="video_link"
)


# -------------------------
# Generate Summary
# -------------------------

if st.button(
    "Generate Summary",
    use_container_width=True
):

    if not link:

        st.warning(
            "Please enter a YouTube link."
        )

    elif not is_valid_syntax(link):

        st.error(
            "Invalid YouTube link."
        )

    elif not is_link_live(link):

        st.warning(
            "Video unavailable / private / deleted."
        )

    else:

        with st.spinner(
            "Analyzing video and generating summary..."
        ):

            transcript = get_transcrpt(link)

            summary = get_summary_gemini(
                transcript
            )

            st.session_state.summary = summary

        st.success(
            "Summary generated successfully!"
        )


# -------------------------
# Summary Section
# -------------------------

if st.session_state.summary:

    st.divider()

    st.subheader("Summary")

    st.write(
        st.session_state.summary
    )

    st.divider()

    # Audio Generation
    if st.button(
        "Generate Audio",
        use_container_width=True
    ):

        with st.spinner(
            "Generating narration..."
        ):

            try:

                audio_bytes = get_sum_tts(
                    st.session_state.summary
                )

                st.audio(
                    audio_bytes,
                    format="audio/wav"
                )

                st.success(
                    "Audio ready!"
                )

            except Exception as e:

                st.error(
                    f"Error: {e}"
                )

    st.divider()

    # Reset Flow
    if st.button(
        "Summarize Another Video",
        use_container_width=True
    ):

        st.session_state.summary = None
        st.session_state.video_link = ""

        st.rerun()