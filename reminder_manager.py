import sqlite3
import datetime
import threading
import time
import tkinter as tk
from tkinter import messagebox

DB_NAME = "reminders.db"


class ReminderManager:
    def __init__(self, speak_function):
        self.speak = speak_function
        self.init_db()
        threading.Thread(target=self.check_reminders, daemon=True).start()

    def init_db(self):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS reminders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT,
                remind_time TEXT
            )
        """)
        conn.commit()
        conn.close()

    def add_reminder(self, text, remind_time):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO reminders (text, remind_time) VALUES (?, ?)",
            (text, remind_time)
        )
        conn.commit()
        conn.close()

    def show_popup(self, message):
        # Create popup window
        root = tk.Tk()
        root.withdraw()  # Hide main window
        messagebox.showinfo("Reminder", message)
        root.destroy()

    def check_reminders(self):
        while True:
            now = datetime.datetime.now().strftime("%H:%M")

            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, text FROM reminders WHERE remind_time=?",
                (now,)
            )
            reminders = cursor.fetchall()

            for reminder_id, text in reminders:
                full_message = f"Reminder: {text}"

                # Speak reminder
                self.speak(full_message)

                # Show popup
                self.show_popup(full_message)

                # Delete after showing
                cursor.execute(
                    "DELETE FROM reminders WHERE id=?",
                    (reminder_id,)
                )
                conn.commit()

            conn.close()
            time.sleep(20)