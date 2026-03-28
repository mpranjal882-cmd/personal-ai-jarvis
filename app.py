from flask import Flask, render_template, request, jsonify
import speech_recognition as sr
import wikipedia, pywhatkit, pyjokes, datetime, os, requests, webbrowser
from fuzzywuzzy import fuzz
import random

app = Flask(__name__)

smart_responses = {
    "how are you": "I'm always here to assist you!",
    "hii":"hello!",
    "who created you": "You did, Pranjal!",
    "what is your name": "I am Jarvis, your assistant.",
    "hello": "Hello! How can I help you today?",
    "good morning": "Good morning! Stay productive.",
    "good night": "Good night! Sweet dreams.",
    "i love you": "Love is beautiful. I'm here for you always.",
    "thank you": "You're welcome!",
    "tell me a joke": pyjokes.get_joke(),
    "what is the time": datetime.datetime.now().strftime('%I:%M %p'),
    "what is the date": datetime.datetime.now().strftime('%B %d, %Y'),
}

quotes = [
    "Success begins with self belief.",
    "Work hard in silence, let success make the noise.",
    "Small steps every day become big achievements.",
    "Your future depends on what you do today.",
    "Never stop learning."
]

def match_command(command):
    command = command.lower().strip()
    for phrase in smart_responses:
        if fuzz.ratio(command, phrase) > 80:
            resp = smart_responses[phrase]
            return resp() if callable(resp) else resp
    return None


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/command", methods=["POST"])
def command():
        text = request.form.get("command_text", "").strip().lower()
        if not text:
            return jsonify({"ok": False, "message": "Empty command"})

        smart_reply = match_command(text)
        if smart_reply:
            return jsonify({"ok": True, "response": smart_reply, "type": "smart"})

        if "motivate me" in text or "motivation" in text:
            return jsonify({"ok": True, "response": random.choice(quotes), "type": "motivation"})

        if "timetable" in text:
            timetable = """
BCA/BSC SEM 3 Timetable

 MONDAY
09:00 - 10:00 → JAVA (RC)
10:00 - 11:00 → PYTHON (DS)
11:30 - 12:30 → LAB JAVA (RC)
02:00 - 04:00 → LAB CLOUD (VB)

 TUESDAY
09:00 - 10:00 → CLOUD (VB)
10:00 - 11:00 → JAVA (RC)
11:30 - 12:30 → PHP (VG)
01:30 - 02:30 → PYTHON (DS)
02:00 - 04:00 → LAB PHP (VG)

 WEDNESDAY
09:00 - 10:00 → JAVA (RC)
10:00 - 11:00 → SE (RC)
11:30 - 12:30 → LAB PYTHON (DS)
12:30 - 01:30 → LAB JAVA (RC)
02:00 - 04:00 → Campus to Corporate (VS/JT)

THURSDAY
09:00 - 10:00 → SE (RC)
10:00 - 11:00 → CLOUD (VB)
12:30 - 01:30 → LAB PYTHON (DS)
02:00 - 03:00 → CLOUD (VB)

 FRIDAY
09:00 - 10:00 → SE (RC)
10:00 - 11:00 → PHP (VG)
12:30 - 01:30 → PYTHON (DS)
02:00 - 04:00 → LIBRARY

 SATURDAY & SUNDAY
Holiday 
"""
            return jsonify({"ok": True, "response": timetable, "type": "timetable"})

        if "wikipedia" in text:
            topic = text.replace("wikipedia", "").strip()
            try:
                result = wikipedia.summary(topic, sentences=2)
                return jsonify({"ok": True, "response": result, "type": "wikipedia"})
            except Exception as e:
                return jsonify({"ok": False, "message": f"Wikipedia error: {e}"})

        if text.startswith("play "):
            query = text.replace("play", "").strip()
            try:
                pywhatkit.playonyt(query)
                return jsonify({"ok": True, "response": f"Playing {query} on YouTube", "type": "play"})
            except Exception as e:
                return jsonify({"ok": False, "message": f"Could not play: {e}"})

        if text.startswith("search "):
            query = text.replace("search", "").strip()
            pywhatkit.search(query)
            return jsonify({"ok": True, "response": f"Searching {query} on Google", "type": "search"})

        if text.startswith("g "):
            query = text.replace("g", "").strip()
            url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
            return jsonify({"ok": True, "response": f"Google Search: {url}", "type": "search", "url": url})

        if "vishal sir" in text:
            return jsonify({"ok": True, "response": "Vishal Sir teaches Cyber Security & Cloud Computing at KN University.", "type": "professor"})

        if "viral sir" in text:
            return jsonify({"ok": True, "response": "Viral Sir teaches PHP & Web Technologies at KN University.", "type": "professor"})

        if "deepak sir" in text:
            return jsonify({"ok": True, "response": "Deepak Sir teaches Python Programming at KN University.", "type": "professor"})

        if "kn university" in text or "about kn university" in text:
            return jsonify({"ok": True, "response": "KN University focuses on modern, practical & industry-oriented education.", "type": "university"})

        if any(op in text for op in ["+", "-", "*", "x", "/", "divide", "multiply", "add", "subtract"]):
            try:
                expr = text.replace("x", "*").replace("divide", "/").replace("multiply", "*").replace("add", "+").replace("subtract", "-")
                result = eval(expr)
                return jsonify({"ok": True, "response": f"Answer: {result}", "type": "math"})
            except:
                return jsonify({"ok": False, "message": "Math error"})

        if "open camera" in text:
            os.system("start microsoft.windows.camera:")
            return jsonify({"ok": True, "response": "Opening Camera...", "type": "camera"})

        if "open calculator" in text:
            os.system("calc")
            return jsonify({"ok": True, "response": "Opening Calculator...", "type": "calculator"})

        if "open notepad" in text:
            os.system("notepad")
            return jsonify({"ok": True, "response": "Opening Notepad...", "type": "notepad"})

        if "open word" in text:
            os.system("start winword")
            return jsonify({"ok": True, "response": "Opening MS Word...", "type": "word"})

        if "open excel" in text:
            os.system("start excel")
            return jsonify({"ok": True, "response": "Opening MS Excel...", "type": "excel"})

        if "open browser" in text:
            webbrowser.open("https://www.google.com")
            return jsonify({"ok": True, "response": "Opening Browser...", "type": "browser"})

        if "open vlc" in text:
            os.system("start vlc")
            return jsonify({"ok": True, "response": "Opening VLC Media Player...", "type": "vlc"})

        return jsonify({"ok": True, "response": "Samajh nahi aaya, fir se boliye.", "type": "fallback"})


if __name__ == "__main__":
    app.run(port=8000, debug=True)
