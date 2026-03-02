import asyncio
import edge_tts
import os
import uuid
import playsound

VOICE = "en-IN-NeerjaNeural"  # Indian English, very clear

async def _speak_async(text):
    filename = f"temp_{uuid.uuid4()}.mp3"
    communicate = edge_tts.Communicate(text, VOICE)
    await communicate.save(filename)
    playsound.playsound(filename)
    os.remove(filename)

def speak(text, speech_rate=150):
    try:
        asyncio.run(_speak_async(text))
    except RuntimeError:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(_speak_async(text))
