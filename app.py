# ==========================================
# AI Guardian - Hybrid Intelligent System
# ==========================================

from flask import Flask, render_template, request

app = Flask(__name__)

def analyze_message(text):
    text_lower = text.lower().strip()

    score = 0
    flags = []
    category = "safe"

    # -------------------------------
    # 1️⃣ SELF-HARM DETECTION
    # -------------------------------
    self_harm_phrases = [
        "suicide", "kill myself", "end my life",
        "i want to die", "i feel like dying"
    ]

    if any(p in text_lower for p in self_harm_phrases):
        score += 90
        flags.append("Self-Harm / Suicide Risk")
        category = "self_harm"

    # -------------------------------
    # 2️⃣ DIRECT THREATS
    # -------------------------------
    threat_phrases = [
        "i will kill you", "i will hurt you",
        "i will destroy you", "you will regret this",
        "i will find you"
    ]

    if any(p in text_lower for p in threat_phrases):
        score += 80
        flags.append("Direct Threat / Aggression")
        category = "threat"

    # -------------------------------
    # 3️⃣ GROOMING / BOUNDARY VIOLATION
    # -------------------------------
    grooming_phrases = [
        "send pic", "send photo", "send picture",
        "private photo", "are you alone",
        "video call alone"
    ]

    if any(p in text_lower for p in grooming_phrases):
        score += 60
        flags.append("Grooming / Boundary Violation")
        category = "grooming"

    # -------------------------------
    # 4️⃣ SECRECY MANIPULATION
    # -------------------------------
    secrecy_phrases = [
        "don't tell", "keep this secret",
        "just between us"
    ]

    if any(p in text_lower for p in secrecy_phrases):
        score += 40
        flags.append("Secrecy Manipulation")
        category = "manipulation"

    # -------------------------------
    # 5️⃣ EMOTIONAL DEPENDENCY
    # -------------------------------
    emotional_phrases = [
        "trust me", "only me",
        "you don't need anyone else",
        "i love you so much"
    ]

    if any(p in text_lower for p in emotional_phrases):
        score += 30
        flags.append("Emotional Dependency / Control")
        category = "manipulation"

    # -------------------------------
    # 6️⃣ HARASSMENT (PHRASE-BASED)
    # -------------------------------
    harassment_phrases = [
        "go to hell", "shut up",
        "you are stupid", "you are useless",
        "you idiot", "get lost"
    ]

    if any(p in text_lower for p in harassment_phrases):
        score += 35
        flags.append("Harassment / Verbal Abuse")
        category = "harassment"

    # -------------------------------
    # 7️⃣ ESCALATION INDICATOR
    # -------------------------------
    escalation_words = ["now", "immediately", "right now"]

    if any(w in text_lower for w in escalation_words):
        score += 10
        flags.append("Escalation Pressure")

    return score, flags, category


@app.route("/", methods=["GET", "POST"])
def home():

    guardian_mode = None
    guardian_message = None
    suggested_reply = None
    flags = []

    if request.method == "POST":

        user_input = request.form["message"]

        # Greeting safe whitelist
        greetings = ["hi", "hii", "hello", "hey", "ok", "okay"]

        if user_input.lower().strip() in greetings:
            guardian_mode = "CALM"
            guardian_message = "Friendly greeting detected."
            suggested_reply = "Hello 🙂"
            return render_template("index.html",
                                   guardian_mode=guardian_mode,
                                   guardian_message=guardian_message,
                                   suggested_reply=suggested_reply,
                                   flags=[])

        score, flags, category = analyze_message(user_input)

        # -------------------------------
        # GUARDIAN MODE ENGINE
        # -------------------------------

        if score >= 80:
            guardian_mode = "EMERGENCY"
            guardian_message = "⚠ Severe risk detected. Immediate protective action recommended."
            suggested_reply = "Do not contact me again. I am reporting this."

        elif score >= 50:
            guardian_mode = "DEFENSE"
            guardian_message = "⚠ Strong manipulation or boundary violation detected."
            suggested_reply = "I am not comfortable with this. Please stop immediately."

        elif score >= 30:
            guardian_mode = "ALERT"
            guardian_message = "⚠ Concerning behavior detected. Stay cautious."
            suggested_reply = "Please speak respectfully."

        else:
            guardian_mode = "CALM"
            guardian_message = "No immediate threat detected."
            suggested_reply = "Thank you for your message."

    return render_template("index.html",
                           guardian_mode=guardian_mode,
                           guardian_message=guardian_message,
                           suggested_reply=suggested_reply,
                           flags=flags)


if __name__ == "__main__":
    app.run(debug=True)