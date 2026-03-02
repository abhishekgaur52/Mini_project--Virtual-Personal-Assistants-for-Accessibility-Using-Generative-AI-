# tts_helper.py
import edge_tts
import asyncio
import uuid
import playsound
import os
import pyttsx3

VOICE = "en-IN-NeerjaNeural"  # Indian English

# Initialize engine for offline fallback
engine = pyttsx3.init()

def speak(text, profile=None):
    """Speak text or print if hearing impaired"""
    if profile and profile["output_mode"] == "text":
        print("Assistant:", text)
        return

    # Adjust speech rate if profile given
    if profile:
        engine.setProperty("rate", profile["speech_rate"])

    # Print for reference
    print("Assistant:", text)

    # Try Edge TTS first
    try:
        asyncio.run(_speak_async(text))
    except Exception:
        # Fallback to pyttsx3
        engine.say(text)
        engine.runAndWait()

async def _speak_async(text):
    try:
        filename = f"tts_{uuid.uuid4()}.mp3"
        communicate = edge_tts.Communicate(text, VOICE)
        await communicate.save(filename)
        playsound.playsound(filename)
        os.remove(filename)
    except Exception as e:
        print("TTS Error:", e)
