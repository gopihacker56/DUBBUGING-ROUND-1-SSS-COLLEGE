import streamlit as st
import time
import pandas as pd
from datetime import datetime

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Online Quiz", layout="centered")
QUIZ_DURATION = 30 * 60
ADMIN_PASSWORD = "admin123"

# ---------------- STYLE ----------------
st.markdown("""
<style>
body { background:#f4f6fb; }
.card {
 background:white;
 padding:15px;
 margin-bottom:15px;
 border-radius:10px;
 box-shadow:0 4px 10px rgba(0,0,0,.1);
}
.timer {
 background:#ffe6e6;
 padding:10px;
 border-radius:8px;
 text-align:center;
 font-weight:bold;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION STATE ----------------
defaults = {
    "started": False,
    "submitted": False,
    "start_time": None,
    "answers": {},
    "force_submit": False,
    "score": 0
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

st.title("📝 Online Quiz Examination")

# ---------------- TAB SWITCH AUTO SUBMIT ----------------
st.components.v1.html("""
<script>
document.addEventListener("visibilitychange", function () {
    if (document.hidden) {
        window.location.href = "?autosubmit=true";
    }
});
</script>
""", height=0)

if "autosubmit" in st.query_params:
    st.session_state.force_submit = True

# ---------------- ADMIN PANEL ----------------
st.sidebar.title("🔐 Admin")
pwd = st.sidebar.text_input("Password", type="password")

if pwd == ADMIN_PASSWORD:
    st.sidebar.success("Admin Access")
    try:
        df = pd.read_csv("results.csv")
        st.subheader("📊 Score Board")
        st.dataframe(df.sort_values("Score", ascending=False))
    except:
        st.info("No results yet")

# ---------------- LOGIN ----------------
if not st.session_state.started:
    st.subheader("Student Details")
    name = st.text_input("Name")
    college = st.text_input("College")

    if st.button("Start Quiz"):
        if not name.strip() or not college.strip():
            st.error("Name & College are required")
        else:
            st.session_state.started = True
            st.session_state.start_time = time.time()
            st.session_state.name = name
            st.session_state.college = college

# ---------------- QUESTIONS ----------------
elif not st.session_state.submitted:

    questions = [
        {"q":"1) 40 men can cut 60 trees in 8 hrs. If 8 men leave the job, how many trees will be cut in 12 hrs?",
         "o":["72 trees","74 trees","68 trees","70 trees"],"a":"72 trees"},
        {"q":"2) Find the wrong number in the series: 1 2 8 24 120 720 5040",
         "o":["8","120","24","720"],"a":"8"},
        {"q":"3) Find the octal value if equivalent of the binary number  1101010111001111 is _____________",
         "o":["152181","153182","152781","152717"],"a":"152717"},
        {"q":"4)  B is sister of A. A is father of C, C is brother of D, How is D related to B ?",
         "o":["Aunt","Nephew","Uncle","Data inadequate"],"a":"Data inadequate"},
        {"q":"5) In a certain code language the word 'PUBLISHED' be written as 'DBUSILEHP'. How will the word 'NUMERICAL' be written in that code language ?",
         "o":["LMUIREACN","LNUIRFACN","MLUIREANL","LUNIRECAN"],"a":"LMUIREACN"},
        {"q":"6) If Y=50 and AT=42 then CAT wil be equal to ___________",
         "o":["39","49","48","58"],"a":"48"},
        {"q":"7) A is taller than B but shoter than C, D is shorter than E & E is not as tall as B. Who should be in the middle if they stand in a row according to height.",
         "o":["A","B","C","D"],"a":"B"},
        {"q":"8) Arrange the given words in alphabetical order R tick the one that comes in the middle.",
         "o":["Evulation","Exchangeable","Exchequee","Execrate"],"a":"Execrate"},
        {"q":"9) The cistern is normally filled in 10 hrs. Due to its leakage it takes 2 hrs extra. If the cistern is full, the leak will empty the tank in?",
         "o":["50 hrs","60 hrs","40 hrs","30 hrs"],"a":"60 hrs"},
        {"q":"10) If 20 notebooks cost Rs.350. What do 29 cost?",
         "o":["Rs.507.50","Rs.501.75","Rs.506.50","Rs.503.25"],"a":"Rs.507.50"},
        {"q":"11) What is the mean proporiton of 0.32 & 0.02 ?",
         "o":["0.8","0.08","0.008","8"],"a":"0.08"},
        {"q":"12) A sum of Rs.1500 is lent at 4% per annum. Find the simple interest for 4 years.",
         "o":["Rs.240","Rs.280","Rs.300","Rs.320"],"a":"Rs.240"},
        {"q":"13) Find the greatest number which when subtracted from 3000 is exactly divisible by 7, 11,13.",
         "o":["1799","1800","1801","1999"],"a":"1999"},
        {"q":"14) The present ages of vikas & vishal are in the ration 15:8. After ten years, their ages will be in the ratio 5:3. Find their present ages.",
         "o":["60,32","70,30","32,72","20,60"],"a":"60,32"},
        {"q":"15) The cost of a bike last year was Rs.19000, Its costs this year is Rs.17000. Find the percentage of decrease in its cost.?",
         "o":["10%","10.5%","12%","12.5%"],"a":"10.5%"},
        {"q":"16) Which loop exectute atleast once?",
         "o":["for","while","do while","continue"],"a":"do while"},
        {"q":"17) What is the size of turbo C/C++ compiler is?",
         "o":["16 Bit","32 Bit","64 Bit","128 Bit"],"a":"16 Bit"},
        {"q":"18) C++ is a ________________ language?",
         "o":["Object Oriented Programming","Semi Object Oriented Programming","Procedural or programming","Structured programming"],"a":"Semi Object Oriented Programming"},
        {"q":"19) Which loop is Fastest in C++?",
         "o":["for","while","do while","All same"],"a":"All same"},
        {"q":"20) Which the key used for trace the statement or debug in a C program?",
         "o":["F1","F9","F11","F7"],"a":"F7"},
        {"q":"21) Which key is used for next error?",
         "o":["Alt+F7","Alt+F8","Ctrl+F8","Ctrl+F7"],"a":"Alt+F8"},
        {"q":"22) Which interface is used to store object in JAVA?",
         "o":["Serializable","Cloneable","Comparable","Runnable"],"a":"Serializable"},
        {"q":"23) Which of hte following statement is TRUE?",
         "o":["JVM dep","JDK indep","Bytecode indep","JRE indep"],"a":"Bytecode indep"},
        {"q":"24) Which method is used to prevent overriding?",
         "o":["Finally","Finalize","Final","Static"],"a":"Final"},
        {"q":"25) Which method is used for Garbage collector?",
         "o":["Finally","Final","Finalize","Destroy"],"a":"Finalize"},
        {"q":"26) Which shortcut permanently exists the python shell?",
         "o":["Ctrl+Q","Ctrl+D","Ctrl+Z","Ctrl+F5"],"a":"Ctrl+Q"},
        {"q":"27) Why Java program throws NullPointerException even though the object was created??",
         "o":["Object went out of scope","Reference was reassigned to null","JVM bug","Garbage collector error"],"a":"Reference was reassigned to null"},
        {"q":"28) 23)A program crashes only when polymorphism is used. What should you check FIRST??",
         "o":["Loop","Virtual function","Header","Compiler flags"],"a":"Virtual function"},
        {"q":"29) Two variables change together even though only one is modified. Why?",
         "o":["Python bug","Variables share the same object reference","Garbage collection","Scope resolution"],"a":"Variables share the same object reference"},
        {"q":"30) A variable changes value without being modified explicitly. What is the MOST probable cause?",
         "o":["Compiler Optimization","Buffer overflow","Wrong datatype","Missing return statement"],"a":"Buffer overflow"}
    ]

    elapsed = int(time.time() - st.session_state.start_time)
    remaining = QUIZ_DURATION - elapsed
    if remaining <= 0:
        st.session_state.force_submit = True

    mins, secs = divmod(max(remaining, 0), 60)
    st.markdown(f"<div class='timer'>⏳ {mins:02d}:{secs:02d}</div>", unsafe_allow_html=True)

    for i, q in enumerate(questions):
        st.markdown("<div class='card'>", unsafe_allow_html=True)

        prev = st.session_state.answers.get(i)
        idx = q["o"].index(prev) if prev in q["o"] else None

        st.session_state.answers[i] = st.radio(
            q["q"], q["o"], index=idx, key=f"q{i}"
        )

        st.markdown("</div>", unsafe_allow_html=True)

    if st.button("Submit") or st.session_state.force_submit:
        score = sum(
            1 for i, q in enumerate(questions)
            if st.session_state.answers.get(i) == q["a"]
        )

        st.session_state.submitted = True
        st.session_state.score = score

        df = pd.DataFrame([{
            "Name": st.session_state.name,
            "College": st.session_state.college,
            "Score": score,
            "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }])

        try:
            old = pd.read_csv("results.csv")
            df = pd.concat([old, df], ignore_index=True)
        except:
            pass

        df.to_csv("results.csv", index=False)
        st.success(f"Submitted! Score: {score}/30")

# ---------------- AFTER SUBMIT ----------------
else:
    st.error("🚫 Exam Finished")
    st.success(f"Final Score: {st.session_state.score}")
