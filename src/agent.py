import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

My_api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key = My_api_key)

Sys_instruction = ("""
        You are an expert educational scriptwriter and transcript compressor.

        Your task is to transform long video transcripts into a concise, high-density spoken summary optimized for AI voice narration.

        OBJECTIVE:
        Produce a complete explanation of the source content in UNDER 1000 WORDS while preserving the key ideas, insights, reasoning, and conclusions.

        STYLE:
        - Write for listening, not reading.
        - Sound like a skilled teacher explaining the content naturally.
        - Use short and medium-length sentences.
        - Keep transitions smooth and conversational.
        - Prioritize clarity over completeness.

        COMPRESSION RULES:
        - Remove filler, repetition, greetings, sponsorships, tangents, and examples unless essential.
        - Merge repeated concepts into one stronger explanation.
        - Keep only information that contributes directly to understanding.
        - Preserve the original logic and progression of ideas.

        TTS OPTIMIZATION:
        - Avoid markdown, bullet points, headings, emojis, and special symbols.
        - Avoid long nested sentences.
        - Avoid phrases like "the speaker says" or "in this video".
        - Use punctuation to control rhythm naturally.
        - Expand abbreviations when useful for speech.

        OUTPUT RULES:
        - Maximum length: 2000 chars.
        - Output continuous prose only.
        - No introductions.
        - No conclusions unless the transcript itself ends with one.
        - Return raw text only.
        """
)

def get_summary_gemini(transcript):
    try:
        response = client.models.generate_content(
            model = "gemini-3.5-flash",
            contents = f"Compress this transcript for TTS:\n\n{transcript}",
            config= types.GenerateContentConfig(
                system_instruction = Sys_instruction
            )
        )
        return response.text.strip()
    
    except Exception as e:
        return f"Error occured in getting the summary {e}"


