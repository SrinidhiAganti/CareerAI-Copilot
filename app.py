from flask import Flask, render_template, request, jsonify
import re

app = Flask(__name__)


CAREER_DATA = {
    "AI / ML Engineer": {
        "skills": [
            "Python",
            "Machine Learning",
            "Deep Learning",
            "NumPy",
            "Pandas",
            "SQL",
            "TensorFlow",
            "NLP"
        ],
        "roadmap": [
            "Strengthen Python programming",
            "Learn NumPy and Pandas",
            "Learn Machine Learning fundamentals",
            "Study Deep Learning and Neural Networks",
            "Learn NLP fundamentals",
            "Build 2 AI/ML projects",
            "Practice technical interviews"
        ]
    },

    "Software Developer": {
        "skills": [
            "Python",
            "Java",
            "Data Structures",
            "Algorithms",
            "SQL",
            "Git",
            "REST APIs",
            "Problem Solving"
        ],
        "roadmap": [
            "Strengthen programming fundamentals",
            "Learn Data Structures and Algorithms",
            "Practice problem solving",
            "Learn SQL and databases",
            "Learn REST APIs",
            "Build full-stack projects",
            "Practice coding interviews"
        ]
    },

    "Cybersecurity Analyst": {
        "skills": [
            "Networking",
            "Linux",
            "Python",
            "Cybersecurity",
            "Cryptography",
            "Web Security",
            "Ethical Hacking",
            "Security Tools"
        ],
        "roadmap": [
            "Learn computer networking",
            "Learn Linux fundamentals",
            "Learn cybersecurity concepts",
            "Study web security",
            "Learn basic cryptography",
            "Practice security labs",
            "Prepare for cybersecurity interviews"
        ]
    }
}


def extract_skills(text):
    skills = [
        "python",
        "java",
        "javascript",
        "c++",
        "sql",
        "machine learning",
        "deep learning",
        "tensorflow",
        "pytorch",
        "numpy",
        "pandas",
        "git",
        "github",
        "html",
        "css",
        "react",
        "node.js",
        "flask",
        "django",
        "linux",
        "networking",
        "cybersecurity",
        "nlp",
        "data structures",
        "algorithms",
        "rest api"
    ]

    text = text.lower()

    found = []

    for skill in skills:
        if skill in text:
            found.append(skill.title())

    return list(dict.fromkeys(found))


def calculate_career_match(student_skills, required_skills):
    student = {skill.lower() for skill in student_skills}

    matched = []
    missing = []

    for skill in required_skills:
        if skill.lower() in student:
            matched.append(skill)
        else:
            missing.append(skill)

    score = round((len(matched) / len(required_skills)) * 100)

    return score, matched, missing


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():

    data = request.get_json()

    resume = data.get("resume", "")
    github = data.get("github", "")
    selected_career = data.get("career", "")

    combined_text = resume + " " + github

    student_skills = extract_skills(combined_text)

    results = {}

    for career, details in CAREER_DATA.items():

        score, matched, missing = calculate_career_match(
            student_skills,
            details["skills"]
        )

        results[career] = {
            "score": score,
            "matched": matched,
            "missing": missing
        }

    best_career = max(
        results,
        key=lambda career: results[career]["score"]
    )

    if selected_career and selected_career in CAREER_DATA:
        recommended_career = selected_career
    else:
        recommended_career = best_career

    selected_result = results[recommended_career]

    readiness_score = selected_result["score"]

    return jsonify({
        "skills": student_skills,
        "recommended_career": recommended_career,
        "career_score": selected_result["score"],
        "matched": selected_result["matched"],
        "missing": selected_result["missing"],
        "roadmap": CAREER_DATA[recommended_career]["roadmap"],
        "readiness_score": readiness_score,
        "all_careers": results
    })


@app.route("/interview", methods=["POST"])
def interview():

    data = request.get_json()

    career = data.get("career", "Software Developer")

    questions = {
        "AI / ML Engineer": [
            "What is supervised learning?",
            "Explain overfitting in machine learning.",
            "What is the difference between classification and regression?",
            "Explain the purpose of a neural network.",
            "What is NLP?"
        ],

        "Software Developer": [
            "What is object-oriented programming?",
            "Explain the difference between an array and a linked list.",
            "What is an API?",
            "What is Git and why is it used?",
            "Explain time complexity."
        ],

        "Cybersecurity Analyst": [
            "What is phishing?",
            "What is encryption?",
            "What is a firewall?",
            "What is the difference between HTTP and HTTPS?",
            "What is multi-factor authentication?"
        ]
    }

    return jsonify({
        "career": career,
        "questions": questions.get(
            career,
            questions["Software Developer"]
        )
    })


@app.route("/feedback", methods=["POST"])
def feedback():

    data = request.get_json()

    answer = data.get("answer", "")

    if not answer.strip():
        return jsonify({
            "score": 0,
            "feedback": "Please provide an answer."
        })

    word_count = len(re.findall(r"\b\w+\b", answer))

    if word_count >= 50:
        score = 9
        feedback = (
            "Good detailed response. Your answer shows "
            "strong understanding. Try adding a practical "
            "example to make it even stronger."
        )

    elif word_count >= 25:
        score = 7
        feedback = (
            "Good response. Add more technical detail "
            "and a practical example."
        )

    elif word_count >= 10:
        score = 5
        feedback = (
            "Your answer has the basic idea. Explain "
            "the concept more clearly and provide an example."
        )

    else:
        score = 3
        feedback = (
            "The answer is too short. Explain the concept "
            "with a definition, key points, and an example."
        )

    return jsonify({
        "score": score,
        "feedback": feedback
    })


if __name__ == "__main__":
    app.run(debug=True)
