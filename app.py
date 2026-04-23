import streamlit as st
import time
import pandas as pd

st.set_page_config(page_title="ICAI CBT System", layout="wide")

st.title("📚 ICAI Advanced ITT Exam Dashboard")

TOTAL_QUESTIONS = 20
EXAM_TIME = 60 * 60  # 60 minutes

# ---------------- SIDEBAR ---------------- #

st.sidebar.title("📌 Select Exam Unit")

unit = st.sidebar.radio(
    "Choose Module",
    ["📊 Unit 1: Power BI", "🐍 Unit 2: Python", "🔷 Unit 3: KNIME"]
)

st.sidebar.markdown("---")
st.sidebar.info("🧠 Select unit to start exam")

# ---------------- QUESTION BANK ---------------- #

powerbi = [
{
"q":"What is Power BI used for?",
"options":["Gaming","Data visualization","Typing","Email"],
"ans":"B",
"exp":"Power BI is used for data visualization."
},
{
"q":"Power BI Desktop is used for?",
"options":["Reports creation","Browsing","Gaming","Music"],
"ans":"A",
"exp":"Used for report creation."
},
]

python = [
{
"q":"Output of 2**3?",
"options":["6","8","9","5"],
"ans":"B",
"exp":"2**3 = 8"
},
{
"q":"Which is immutable?",
"options":["List","Tuple","Set","Dict"],
"ans":"B",
"exp":"Tuple is immutable"
},
]

knime = [
{
"q":"KNIME is used for?",
"options":["Gaming","Data analytics","Music","Typing"],
"ans":"B",
"exp":"KNIME is a data analytics tool"
},
{
"q":"What are nodes in KNIME?",
"options":["Files","Processing blocks","Images","Tables"],
"ans":"B",
"exp":"Nodes perform operations"
},
]

# ---------------- UNIT SELECT ---------------- #

if "Unit 1" in unit:
    base_questions = powerbi
elif "Unit 2" in unit:
    base_questions = python
else:
    base_questions = knime

questions = []
for i in range(TOTAL_QUESTIONS):
    questions.append(base_questions[i % len(base_questions)].copy())

# ---------------- SESSION ---------------- #

if "started" not in st.session_state:
    st.session_state.started = False

def reset():
    st.session_state.index = 0
    st.session_state.answers = [None]*TOTAL_QUESTIONS
    st.session_state.start_time = time.time()
    st.session_state.submitted = False
    st.session_state.started = True

# ---------------- START ---------------- #

if not st.session_state.started:
    if st.button("🚀 Start Exam"):
        reset()

# ---------------- EXAM SCREEN ---------------- #

if st.session_state.started and not st.session_state.submitted:

    elapsed = int(time.time() - st.session_state.start_time)
    remaining = EXAM_TIME - elapsed

    if remaining <= 0:
        st.session_state.submitted = True

    mins = max(0, remaining // 60)
    secs = max(0, remaining % 60)

    st.markdown(f"### ⏳ Time Left: {mins:02d}:{secs:02d}")

    i = st.session_state.index
    q = questions[i]

    st.markdown(f"### Question {i+1} / {TOTAL_QUESTIONS}")
    st.info(q["q"])

    choice = st.radio(
        "Select answer:",
        ["A","B","C","D"],
        index=["A","B","C","D"].index(st.session_state.answers[i]) if st.session_state.answers[i] else None,
        format_func=lambda x: f"{x}) {q['options'][ord(x)-65]}"
    )

    st.session_state.answers[i] = choice

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("⬅️ Prev") and i > 0:
            st.session_state.index -= 1

    with col2:
        if st.button("➡️ Next") and i < TOTAL_QUESTIONS - 1:
            st.session_state.index += 1

    with col3:
        if st.button("🚨 Submit"):
            st.session_state.submitted = True

    st.markdown("---")

    if st.button("🔄 Reset"):
        reset()

# ---------------- RESULT DASHBOARD ---------------- #

if st.session_state.started and st.session_state.submitted:

    score = 0

    for i, q in enumerate(questions):
        if st.session_state.answers[i] == q["ans"]:
            score += 1

    accuracy = (score / TOTAL_QUESTIONS) * 100

    st.success(f"🎉 {unit} Completed!")

    # ---------------- BEAUTIFUL STATS ---------------- #

    col1, col2, col3 = st.columns(3)

    col1.metric("📊 Score", f"{score}/{TOTAL_QUESTIONS}")
    col2.metric("🎯 Accuracy", f"{accuracy:.2f}%")
    col3.metric("🧠 Status",
                "Excellent 🏆" if accuracy == 100 else
                "Good 👍" if accuracy >= 70 else
                "Needs Improvement 📚")

    st.markdown("---")

    # ---------------- GRAPH ---------------- #

    chart_data = pd.DataFrame({
        "Performance": ["Correct", "Wrong"],
        "Count": [score, TOTAL_QUESTIONS - score]
    })

    st.bar_chart(chart_data.set_index("Performance"))

    st.markdown("---")

    # ---------------- REVIEW ---------------- #

    st.markdown("## 📖 Answer Review")

    for i, q in enumerate(questions):

        st.markdown(f"### Q{i+1}")
        st.write(q["q"])

        user = st.session_state.answers[i]
        correct = q["ans"]

        if user == correct:
            st.success(f"✔ Correct Answer: {user}")
        else:
            st.error(f"❌ Your Answer: {user} | Correct: {correct}")

        st.info(q["exp"])
        st.markdown("---")

    if st.button("🔄 Restart Exam"):
        reset()