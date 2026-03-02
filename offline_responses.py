# offline_responses.py
import datetime

def offline(user_input, profile=None):
    q = user_input.lower()

    if q in ("hello", "hi"):
        return "Hello. How can I help you?"

    if "your name" in q:
        return "I am your accessibility assistant."

    if "time" in q:
        return datetime.datetime.now().strftime("It is %I:%M %p.")

    if "date" in q:
        return datetime.datetime.now().strftime("Today is %B %d, %Y.")

    if "joke" in q:
        return "Why did the computer go to the doctor? Because it caught a virus!"

    return None   # 🔥 VERY IMPORTANT
