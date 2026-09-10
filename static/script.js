let currentCareer = "";
let interviewQuestions = [];
let currentQuestion = 0;


async function analyzeProfile() {

    const resume = document.getElementById("resume").value;
    const github = document.getElementById("github").value;
    const career = document.getElementById("career").value;


    if (!resume && !github) {

        alert("Please enter your resume or GitHub information.");

        return;
    }


    const response = await fetch("/analyze", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            resume: resume,
            github: github,
            career: career
        })

    });


    const data = await response.json();


    currentCareer = data.recommended_career;


    document.getElementById("dashboard")
        .classList.remove("hidden");


    document.getElementById("careerName")
        .innerText = data.recommended_career;


    document.getElementById("careerScore")
        .innerText = data.career_score + "%";


    document.getElementById("readinessScore")
        .innerText = data.readiness_score + "%";


    document.getElementById("skillCount")
        .innerText = data.skills.length;


    renderTags(
        "skills",
        data.skills
    );


    renderTags(
        "missing",
        data.missing
    );


    const roadmap =
        document.getElementById("roadmap");

    roadmap.innerHTML = "";


    data.roadmap.forEach(step => {

        const li =
            document.createElement("li");

        li.innerText = step;

        roadmap.appendChild(li);

    });


    window.scrollTo({
        top: document.getElementById("dashboard").offsetTop,
        behavior: "smooth"
    });

}


function renderTags(elementId, items) {

    const container =
        document.getElementById(elementId);

    container.innerHTML = "";


    items.forEach(item => {

        const span =
            document.createElement("span");

        span.innerText = item;

        container.appendChild(span);

    });

}


async function startInterview() {

    const response = await fetch("/interview", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            career: currentCareer
        })

    });


    const data = await response.json();


    interviewQuestions = data.questions;

    currentQuestion = 0;


    document.getElementById("interviewBox")
        .classList.remove("hidden");


    showQuestion();

}


function showQuestion() {

    document.getElementById("question")
        .innerText =
        "Question " +
        (currentQuestion + 1) +
        ": " +
        interviewQuestions[currentQuestion];


    document.getElementById("answer")
        .value = "";


    document.getElementById("feedback")
        .innerHTML = "";

}


async function submitAnswer() {

    const answer =
        document.getElementById("answer").value;


    const response = await fetch("/feedback", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            answer: answer
        })

    });


    const data = await response.json();


    document.getElementById("feedback")
        .innerHTML =
        "<strong>Score: " +
        data.score +
        "/10</strong><br><br>" +
        data.feedback;


    setTimeout(() => {

        currentQuestion++;


        if (currentQuestion < interviewQuestions.length) {

            showQuestion();

        } else {

            document.getElementById("question")
                .innerText =
                "🎉 Mock Interview Completed!";

        }

    }, 3000);

}
