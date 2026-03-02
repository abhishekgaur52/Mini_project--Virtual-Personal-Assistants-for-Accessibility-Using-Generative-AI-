import speech_recognition as sr
from dateutil import parser
import re

from tts_helper import speak
from offline_responses import offline
from system_commands import execute_command
from context_manager import ContextManager
from llm_handler import ask_ai
from accessibility_profile import AccessibilityProfile
from reminder_manager import ReminderManager


def parse_time_safely(time_input):
    """
    Robust time parsing:
    Handles:
    2305
    18 30
    6 PM
    6:30 PM
    11
    10 45 PM
    """

    time_input = time_input.lower().replace(".", "").strip()

    # Remove words like am/pm spacing issues
    time_input = time_input.replace("a m", "am").replace("p m", "pm")

    # Case 1: 4 digit military time like 2305
    digits_only = re.sub(r"\D", "", time_input)
    if digits_only.isdigit() and len(digits_only) == 4:
        hour = int(digits_only[:2])
        minute = int(digits_only[2:])
        if 0 <= hour <= 23 and 0 <= minute <= 59:
            return f"{hour:02d}:{minute:02d}"

    # Case 2: Single number like "11"
    if time_input.isdigit():
        hour = int(time_input)
        if 0 <= hour <= 23:
            return f"{hour:02d}:00"

    # Case 3: Natural language
    parsed = parser.parse(time_input)
    return parsed.strftime("%H:%M")


def main():
    profile_obj = AccessibilityProfile(disability_type="visual")
    profile = profile_obj.get_profile()

    r = sr.Recognizer()
    mic = sr.Microphone()
    context = ContextManager()

    reminder_manager = ReminderManager(lambda text: speak(text, profile))

    with mic as source:
        r.adjust_for_ambient_noise(source, duration=1)

    speak("Accessibility assistant started. Say exit to stop.", profile)

    while True:
        try:
            with mic as source:
                print("🎤 Listening...")
                audio = r.listen(source, phrase_time_limit=6)

            user = r.recognize_google(audio)
            print("You said:", user)

            user_lower = user.lower()

            # EXIT
            if user_lower == "exit":
                speak("Goodbye.", profile)
                break

            # ==========================
            # REMINDER SECTION
            # ==========================
            if "set reminder" in user_lower:
                speak("What should I remind you?", profile)

                with mic as source:
                    task_audio = r.listen(source, phrase_time_limit=6)
                task = r.recognize_google(task_audio)
                print("Task:", task)

                speak("At what time?", profile)

                with mic as source:
                    time_audio = r.listen(source, phrase_time_limit=6)
                time_input = r.recognize_google(time_audio)
                print("Time spoken:", time_input)

                try:
                    formatted_time = parse_time_safely(time_input)
                    print("Formatted time:", formatted_time)

                    reminder_manager.add_reminder(task, formatted_time)
                    speak(f"Reminder set for {formatted_time}.", profile)

                except Exception as e:
                    print("Time parse error:", e)
                    speak(
                        "Invalid time format. Please say something like 6 PM, 18 30 or 2305.",
                        profile
                    )

                continue

            # ==========================
            # SYSTEM COMMANDS
            # ==========================
            answer = execute_command(user, context)

            # OFFLINE RESPONSES
            if answer is None:
                answer = offline(user)

            # AI RESPONSE
            if answer is None:
                answer = ask_ai(user)

            if answer:
                speak(answer, profile)

        except sr.UnknownValueError:
            speak("Sorry, I did not understand.", profile)

        except Exception as e:
            print("Error:", e)
            speak("Something went wrong.", profile)


if __name__ == "__main__":
    main()
    
    
    
# run commands
# $env:GOOGLE_API_KEY="AIzaSyCQgVbhvTX5hYBTwcpdPhT25FdmtdZNOGM"
# python main.py