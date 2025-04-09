from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

# Function to greet the user based on the time of day
def greet():
    current_hour = datetime.now().hour
    if current_hour < 12:
        return "🌅 Good morning"
    elif current_hour < 18:
        return "🌤️ Good afternoon"
    else:
        return "🌙 Good evening"

# Detect symptoms based on user input
def detect_symptom(user_input):
    user_input = user_input.lower()
    if "cough" in user_input or "throat" in user_input:
        return "cough"
    elif "head" in user_input or "migraine" in user_input:
        return "headache"
    elif "fever" in user_input or "temperature" in user_input:
        return "fever"
    elif "stomach" in user_input or "nausea" in user_input or "vomit" in user_input:
        return "stomachache"
    elif "tired" in user_input or "fatigue" in user_input:
        return "tiredness"
    elif "cramps" in user_input:
        if "muscle" in user_input:
            return "muscle cramps"
        else:
            return "cramps"
    elif "pain" in user_input:
        return "muscle pain"
    elif "breath" in user_input or "asthma" in user_input:
        return "breathing difficulty"
    else:
        return "unknown"

# Function to give advice based on detected symptom
def give_advice(symptom):
    advice = {
        "cough": "💡 Drink warm fluids, rest, and avoid cold air. If it lasts more than 5 days, consult a doctor.",
        "headache": "💡 Rest in a quiet room, drink water, and avoid screen time.",
        "fever": "💡 Stay hydrated, rest, and monitor your temperature. See a doctor if it gets too high.",
        "stomachache": "💡 Eat light food, avoid greasy snacks. If pain is severe, visit a clinic.",
        "tiredness": "💡 Sleep well, eat nutritious food, and take short breaks during the day.",
        "muscle pain": "💡 Try gentle stretching, rest the area, and apply a warm compress.",
        "breathing difficulty": "💡 Stay calm, sit upright, and use an inhaler if prescribed. Seek emergency help if it worsens.",
        "muscle cramps": "💡 For muscle cramps, try stretching, applying a warm compress, or gentle massage.",
        "cramps": "💡 Are you on your period? If so, try using a heat pack on your lower abdomen.",
        "unknown": "❓ Hmm, I couldn't understand that. Try mentioning a common symptom like 'headache' or 'fever'."
    }

    return advice.get(symptom, "❓ I couldn't find advice for that symptom.")

# Function for the risk calculator
def risk_calculator(answers):
    score = 0
    if answers.get('q1') == 'yes':
        score += 2
    if answers.get('q2') == 'yes':
        score += 2
    if answers.get('q3') == 'yes':
        score += 3
    if answers.get('q4') == 'yes':
        score += 1
    if answers.get('q5') == 'yes':
        score += 2

    if score <= 2:
        return "🟢 Low risk. Keep taking care of yourself."
    elif score <= 5:
        return "🟡 Moderate risk. Rest well and monitor your health."
    else:
        return "🔴 High risk. Please consider seeing a healthcare professional."

# Route for greeting page
@app.route("/", methods=["GET", "POST"])
def index():
    greeting = greet()
    return render_template("index.html", greeting=greeting)

# Route for the next page, where they choose between symptom advice or risk calculation
@app.route("/choose", methods=["GET", "POST"])
def choose():
    if request.method == "POST":
        if request.form["choice"] == "advice":
            return redirect(url_for('symptom_input'))
        elif request.form["choice"] == "risk":
            return redirect(url_for('risk_input'))
    return render_template("choose.html")

# Route for symptom input
@app.route("/symptom_input", methods=["GET", "POST"])
def symptom_input():
    if request.method == "POST":
        symptom = request.form["symptom"]
        detected_symptom = detect_symptom(symptom)
        advice = give_advice(detected_symptom)

        # If breathing difficulty is detected, offer breathing exercises
        if detected_symptom == "breathing difficulty":
            return redirect(url_for('breathing_exercises'))

        return render_template("advice.html", advice=advice)

    return render_template("symptom_input.html")

# Route for risk input
@app.route("/risk_input", methods=["GET", "POST"])
def risk_input():
    if request.method == "POST":
        answers = request.form
        risk_level = risk_calculator(answers)
        return render_template("risk.html", risk_level=risk_level)
    return render_template("risk_input.html")

# Route for breathing exercises page (Step 1)
@app.route("/breathing_exercises", methods=["GET", "POST"])
def breathing_exercises():
    return render_template("breathing_exercises.html")

# Route for asking if they want to do something else
@app.route("/ask_again", methods=["GET", "POST"])
def ask_again():
    if request.method == "POST":
        continue_action = request.form.get("continue_action")
        if continue_action == "no":
            return redirect(url_for('thank_you'))
        else:
            return redirect(url_for('choose'))  # Go back to choose options
    return render_template("ask_again.html")

# Route for thank you page
@app.route("/thank_you", methods=["GET", "POST"])
def thank_you():
    return render_template("thank_you.html")

if __name__ == "__main__":
    app.run(debug=True, port=5001)
