import streamlit as st
import time

st.set_page_config(page_title="Python Mock Test PRO", layout="wide")

st.title("📝 Python Mock Test (5 Questions - PRO)")

TOTAL_QUESTIONS = 5
EXAM_TIME = 15 * 60  # 15 minutes

# ---------------- QUESTION BANK ---------------- #

questions = [
{
"q":"What will be the output?\n\nprint(2 + 3 * 4)",
"options":["14","20","24","Error"],
"ans":"A",
"exp":"Multiplication is done first → 3*4=12 → 12+2=14"
},
{
"q":"Which of the following is immutable?",
"options":["List","Set","Dictionary","Tuple"],
"ans":"D",
"exp":"Tuple cannot be changed after creation"
},
{
"q":"What is output?\n\nprint(bool([]))",
"options":["True","False","Error","None"],
"ans":"B",
"exp":"Empty list is considered False"
},
{
"q":"Which keyword is used to define a function?",
"options":["function","def","fun","lambda"],
"ans":"B",
"exp":"def is used to define functions"
},
{
"q":"What is output?\n\nprint('5' + '6')",
"options":["11","56","Error","None"],
"ans":"B",
"exp":"String concatenation → '5' + '6' = '56'"
},
]

# ---------------- SESSION STATE ---------------- #

if "started" not in st.session_state:
    st.session_state.started = False

if not st.session_state.started:
    if st.button("🚀 Start Exam"):
        st.session_state.started = True
        st.session_state.index = 0
        st.session_state.answers = [None]*TOTAL_QUESTIONS
        st.session_state.start_time = time.time()

# ---------------- EXAM SCREEN ---------------- #

if st.session_state.started:

    # TIMER
    elapsed = int(time.time() - st.session_state.start_time)
    remaining = EXAM_TIME - elapsed

    if remaining <= 0:
        st.warning("⏰ Time is over! Auto submitting...")
        submit_now = True
    else:
        mins = remaining // 60
        secs = remaining % 60
        st.markdown(f"### ⏳ Time Left: {mins:02d}:{secs:02d}")
        submit_now = False

    i = st.session_state.index
    q = questions[i]

    st.markdown(f"### Question {i+1} of {TOTAL_QUESTIONS}")
    st.info(q["q"])

    choice = st.radio(
        "Select your answer:",
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
        if st.button("🚨 Submit Test"):
            submit_now = True

# ---------------- RESULT SCREEN ---------------- #

if st.session_state.started and (submit_now):

    score = 0

    for i, q in enumerate(questions):
        if st.session_state.answers[i] == q["ans"]:
            score += 1

    st.success("🎉 Exam Completed Successfully!")

    # ---------------- FINAL RESULT ---------------- #

    st.markdown("## 📊 Result Summary")

    if score == 5:
        st.success("🏆 Excellent! Perfect Score!")
    elif score >= 3:
        st.info("👍 Good Job! You have a strong understanding.")
    else:
        st.warning("📚 Keep Practicing! You can improve.")

    st.markdown(f"### 🎯 Score: {score}/5")
    st.markdown(f"### 📈 Accuracy: {(score/5)*100:.0f}%")

    # ---------------- REVIEW ---------------- #

    st.markdown("---")
    st.markdown("## 📖 Review with Explanations")

    for i, q in enumerate(questions):

        st.markdown(f"### Q{i+1}: {q['q']}")

        user = st.session_state.answers[i]
        correct = q["ans"]

        if user == correct:
            st.success(f"✅ Correct Answer: {correct}")
        else:
            st.error(f"❌ Your Answer: {user} | Correct Answer: {correct}")

        st.info(f"💡 Explanation: {q['exp']}")
        st.markdown("---")