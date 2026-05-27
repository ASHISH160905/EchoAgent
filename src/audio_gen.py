import os
import base64
from dotenv import load_dotenv
from sarvamai import SarvamAI
from sarvamai.play import save

load_dotenv()

My_api_key = os.getenv("SARVAM_API_KEY")

client  = SarvamAI(
     api_subscription_key= My_api_key,
)

def get_sum_tts(sum_trxpt):
    audio = client.text_to_speech.convert(
    model="bulbul:v3",
    text= sum_trxpt,
    target_language_code="en-IN",
    speaker="sumit",
    )
    #save(audio, "output1.wav")
    #return audio
    try:
        base64_audio_str = audio.audios[0]
    except(TypeError , AttributeError):
        base64_audio_str = audio["audios"][0]

    audio_bytes = base64.b64decode(base64_audio_str)
    return audio_bytes

