import streamlit as st
import time

st.set_page_config(page_title="ICAI Mock Test System", layout="wide")

st.title("📚 ICAI Advanced ITT Mock Test (Unit 1 + 2 + 3)")

TOTAL_QUESTIONS = 20
EXAM_TIME = 60 * 60  # 60 minutes

# ---------------- UNIT SELECTION ---------------- #

unit = st.selectbox(
    "Select Unit",
    ["Unit 1: Power BI", "Unit 2: Python", "Unit 3: KNIME"]
)

# ---------------- UNIT 1: POWER BI ---------------- #

powerbi_questions = [
{
"q":"What is Power BI used for?",
"options":["Gaming","Data visualization","Video editing","Emailing"],
"ans":"B",
"exp":"Power BI is a BI tool for visualization."
},
{
"q":"Power BI Desktop is used for?",
"options":["Creating reports","Browsing","Gaming","Coding OS"],
"ans":"A",
"exp":"Used to create reports and dashboards."
},
]

# ---------------- UNIT 2: PYTHON ---------------- #

python_questions = [
{
"q":"What will be output?\nprint(2*3**2)",
"options":["36","18","12","9"],
"ans":"B",
"exp":"3**2=9, 2*9=18"
},
{
"q":"Which is immutable?",
"options":["List","Set","Tuple","Dict"],
"ans":"C",
"exp":"Tuple cannot be changed"
},
]

# ---------------- UNIT 3: KNIME ---------------- #

knime_questions = [
{
"q":"KNIME is used for?",
"options":["Video editing","Data analytics","Gaming","Typing"],
"ans":"B",
"exp":"KNIME is a data analytics platform"
},
{
"q":"What are KNIME nodes?",
"options":["Files","Processing blocks","Images","Reports"],
"ans":"B",
"exp":"Nodes perform data operations"
},
]

# ---------------- SELECT UNIT ---------------- #

if unit == "Unit 1: Power BI":
    base_questions = powerbi_questions
elif unit == "Unit 2: Python":
    base_questions = python_questions
else:
    base_questions = knime_questions

# expand to 20 questions
questions = []
for i in range(TOTAL_QUESTIONS):
    questions.append(base_questions[i % len(base_questions)].copy())

# ---------------- RESET FUNCTION ---------------- #

def reset_exam():
    st.session_state.index = 0
    st.session_state.answers = [None]*TOTAL_QUESTIONS
    st.session_state.start_time = time.time()
    st.session_state.submitted = False
    st.session_state.started = True

# ---------------- START ---------------- #

if "started" not in st.session_state:
    st.session_state.started = False

if not st.session_state.started:
    if st.button("🚀 Start ICAI Exam"):
        reset_exam()

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

    st.markdown(f"### Question {i+1} of {TOTAL_QUESTIONS}")
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
        if st.button("⬅️ Previous") and i > 0:
            st.session_state.index -= 1

    with col2:
        if st.button("➡️ Next") and i < TOTAL_QUESTIONS - 1:
            st.session_state.index += 1

    with col3:
        if st.button("🚨 Submit Exam"):
            st.session_state.submitted = True

    st.markdown("---")

    if st.button("🔄 Reset Exam"):
        reset_exam()

# ---------------- RESULT ---------------- #

if st.session_state.started and st.session_state.submitted:

    score = 0

    for i, q in enumerate(questions):
        if st.session_state.answers[i] == q["ans"]:
            score += 1

    st.success(f"🎉 {unit} Completed!")

    accuracy = (score / TOTAL_QUESTIONS) * 100

    if accuracy == 100:
        st.success("🏆 Outstanding Performance!")
    elif accuracy >= 70:
        st.info("👍 Good Knowledge")
    else:
        st.warning("📚 Needs Improvement")

    st.markdown(f"### 🎯 Score: {score}/{TOTAL_QUESTIONS}")
    st.markdown(f"### 📊 Accuracy: {accuracy:.2f}%")

    st.markdown("---")
    st.markdown("## 📖 Review Answers")

    for i, q in enumerate(questions):

        st.markdown(f"### Q{i+1}")
        st.write(q["q"])

        user = st.session_state.answers[i]
        correct = q["ans"]

        if user == correct:
            st.success(f"✔ Correct ({user})")
        else:
            st.error(f"❌ Your: {user} | Correct: {correct}")

        st.info(q["exp"])
        st.markdown("---")

    if st.button("🔄 Restart Exam"):
        reset_exam()