# voice.py  — FINAL WORKING VERSION
import speech_recognition as sr
from elevenlabs import ElevenLabs, Voice, VoiceSettings
import pygame
import io


# --------------------------------------
# 1. Speech-to-Text
# --------------------------------------
def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening...")
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio)
        print("👂 You said:", text)
        return text.lower()
    except:
        print("❌ Could not understand audio")
        return ""


# --------------------------------------
# 2. Text-to-Speech (Handles ELEVENLABS properly)
# --------------------------------------

ELEVEN_API_KEY = os.getenv("ELEVENLABS_API_KEY")

VOICE_ID = "pNInz6obpgDQGcFmaJgB"   # You can change to any ElevenLabs voice


def speak(text):
    print("🗣 Twin (speaking):", text)

    # Generate audio as REAL bytes
    audio_bytes = client.text_to_speech.convert(
        voice_id=VOICE_ID,
        text=text,
        output_format="mp3_44100_128",
        voice_settings=VoiceSettings(stability=0.3, similarity_boost=0.8)
    )

    # Convert generator → bytes
    audio_data = b"".join(audio_bytes)

    # Initialize pygame audio
    pygame.mixer.init()
    pygame.mixer.music.load(io.BytesIO(audio_data))
    pygame.mixer.music.play()

    # Keep playing until finished
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
