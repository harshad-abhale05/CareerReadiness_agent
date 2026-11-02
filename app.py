```python
import json
from pathlib import Path
import pandas as pd
import streamlit as st

# --------------------------------------------------
# 1. LOAD PROJECT DATA
# --------------------------------------------------

ROOT = Path(__file__).parent

with open(ROOT / "data" / "questions.json", encoding="utf-8") as f:
    QUESTIONS = json.load(f)

with open(ROOT / "data" / "company_requirements.json", encoding="utf-8") as f:
    COMPANIES = json.load(f)

DOMAINS = list(dict.fromkeys(q["domain"] for q in QUESTIONS))

if not QUESTIONS:
    st.error("No questions found in data/questions.json")
    st.stop()

if not COMPANIES:
    st.error("No company requirements found.")
    st.stop()


# --------------------------------------------------
# 2. PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="PrepPath | Placement Readiness",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)


# --------------------------------------------------
# 3. DARK THEME
# --------------------------------------------------

st.markdown("""
<style>
:root {
    --bg: #0b0e14;
    --side: #10141d;
    --card: #121720;
    --border: #252d3a;
    --text: #edf1f8;
    --muted: #8995a8;
    --gold: #f5bd35;
    --teal: #2dd4bf;
    --red: #fa7567;
    --purple: #9b8cff;
}

.stApp {
    background: var(--bg);
    color: var(--text);
}

[data-testid="stHeader"] {
    background: rgba(11,14,20,.96);
}

.block-container {
    max-width: 1500px;
    padding-top: 1.6rem;
    padding-bottom: 2rem;
}

section[data-testid="stSidebar"] {
    background: var(--side);
    border-right: 1px solid var(--border);
}

section[data-testid="stSidebar"] * {
    color: var(--text);
}

.brand {
    display: flex;
    align-items: center;
    gap: 11px;
    padding: 8px 5px 27px;
}

.brand-icon {
    width: 39px;
    height: 39px;
    border-radius: 10px;
    background: var(--gold);
    color: #15120a !important;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 900;
}

.brand-name {
    font-size: 17px;
    font-weight: 800;
}

.brand-sub {
    font-size: 11px;
    color: var(--muted) !important;
}

.heading {
    font-size: 27px;
    font-weight: 800;
    color: #f1f4fa;
}

.subheading {
    font-size: 13px;
    color: var(--muted);
    margin-top: 5px;
}

.crumb {
    font-size: 12px;
    color: var(--muted);
    margin-bottom: 7px;
}

.panel {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 13px;
    padding: 18px;
    margin-bottom: 15px;
}

.panel-title {
    font-size: 15px;
    font-weight: 750;
    color: #f1f4f9;
}

.panel-sub {
    font-size: 11px;
    color: var(--muted);
    margin-top: 4px;
}

.metric {
    background: var(--card);
    border: 1px solid var(--border);
    border-left: 3px solid var(--gold);
    border-radius: 12px;
    padding: 15px;
    min-height: 105px;
}

.metric.teal {
    border-left-color: var(--teal);
}

.metric.red {
    border-left-color: var(--red);
}

.metric-label {
    font-size: 10px;
    color: var(--muted);
}

.metric-value {
    font-size: 26px;
    font-weight: 800;
    margin-top: 8px;
}

.metric-help {
    font-size: 11px;
    color: var(--muted);
    margin-top: 4px;
}

.skill {
    margin-top: 17px;
}

.skill-head {
    display: flex;
    justify-content: space-between;
    font-size: 12px;
    margin-bottom: 7px;
}

.track {
    height: 7px;
    background: #252d3a;
    border-radius: 20px;
    overflow: hidden;
}

.fill {
    height: 100%;
    border-radius: 20px;
    background: var(--teal);
}

.item {
    display: flex;
    align-items: center;
    gap: 11px;
    padding: 13px 0;
    border-bottom: 1px solid var(--border);
}

.item-title {
    font-size: 12px;
    font-weight: 700;
}

.item-detail {
    font-size: 10px;
    color: var(--muted);
    margin-top: 4px;
}

.logo {
    width: 35px;
    height: 35px;
    flex-shrink: 0;
    border-radius: 9px;
    background: #1c2432;
    color: var(--gold);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 11px;
    font-weight: 800;
}

.item-main {
    flex: 1;
    min-width: 0;
}

.badge {
    padding: 5px 9px;
    border-radius: 20px;
    font-size: 10px;
    color: var(--teal);
    background: #12312f;
}

div.stButton > button {
    background: #171e29;
    color: #e9eef7;
    border: 1px solid #303949;
    border-radius: 8px;
}

div.stButton > button:hover {
    border-color: var(--gold);
    color: var(--gold);
}

div.stButton > button[kind="primary"] {
    background: var(--gold);
    color: #15120a;
    border: 1px solid var(--gold);
    font-weight: 800;
}

.stTextInput input,
.stSelectbox div[data-baseweb="select"] > div {
    background: #151b25;
    color: var(--text);
}

@media(max-width: 900px) {
    .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
    }

    .heading {
        font-size: 22px;
    }
}
</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# 4. SESSION STATE
# --------------------------------------------------

defaults = {
    "student": "Harshad Abhale",
    "company": list(COMPANIES.keys())[0],
    "role": list(COMPANIES[list(COMPANIES.keys())[0]].keys())[0],
    "answers": {},
    "submitted": False,
    "attempt": 0
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# --------------------------------------------------
# 5. HELPER FUNCTIONS
# --------------------------------------------------

def calculate_results(answers):

    total = len(QUESTIONS)

    score = sum(
        1 for q in QUESTIONS
        if answers.get(q["id"]) == q["correct_answer"]
    )

    percentage = (score / total) * 100 if total else 0

    rows = []

    for domain in DOMAINS:

        domain_questions = [
            q for q in QUESTIONS
            if q["domain"] == domain
        ]

        correct = sum(
            1 for q in domain_questions
            if answers.get(q["id"]) == q["correct_answer"]
        )

        domain_score = (
            correct / len(domain_questions) * 100
            if domain_questions else 0
        )

        rows.append({
            "Domain": domain,
            "Score": round(domain_score, 1),
            "Correct": f"{correct}/{len(domain_questions)}"
        })

    return score, round(percentage, 1), rows


def metric(label, value, help_text, accent=""):

    st.markdown(
        f"""
        <div class="metric {accent}">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-help">{help_text}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# --------------------------------------------------
# 6. DASHBOARD
# --------------------------------------------------

def dashboard():

    st.markdown(
        f"""
        <div class="crumb">Home / Dashboard</div>
        <div class="heading">
            Welcome back, {st.session_state.student.split()[0]}
        </div>
        <div class="subheading">
            Here's where your placement readiness stands today.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    if st.session_state.submitted:

        score, percentage, rows = calculate_results(
            st.session_state.answers
        )

        cols = st.columns(4)

        with cols[0]:
            metric("READINESS SCORE", f"{percentage}/100",
                   "Based on your assessment")

        with cols[1]:
            metric("CORRECT ANSWERS",
                   f"{score}/{len(QUESTIONS)}",
                   "Assessment performance", "teal")

        with cols[2]:
            metric("DOMAINS ASSESSED",
                   str(len(DOMAINS)),
                   "Technical knowledge")

        gaps = sum(1 for r in rows if r["Score"] < 60)

        with cols[3]:
            metric("SKILL GAPS",
                   str(gaps),
                   "Domains below 60%", "red")

        st.write("")

        left, right = st.columns([1.5, 1])

        with left:

            st.markdown(
                '<div class="panel">'
                '<div class="panel-title">Your technical skills</div>'
                '<div class="panel-sub">Based on your actual assessment results</div>',
                unsafe_allow_html=True
            )

            for row in rows:

                st.markdown(
                    f"""
                    <div class="skill">
                        <div class="skill-head">
                            <b>{row['Domain']}</b>
                            <span>{row['Score']}%</span>
                        </div>
                        <div class="track">
                            <div class="fill"
                                 style="width:{row['Score']}%">
                            </div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            st.markdown("</div>", unsafe_allow_html=True)

        with right:

            st.markdown(
                '<div class="panel">'
                '<div class="panel-title">Assessment status</div>'
                '<div class="panel-sub">Your latest submitted assessment</div>',
                unsafe_allow_html=True
            )

            st.success("Assessment completed successfully.")

            st.write(f"**Target company:** {st.session_state.company}")
            st.write(f"**Target role:** {st.session_state.role}")
            st.write(f"**Readiness:** {percentage}%")

            st.markdown("</div>", unsafe_allow_html=True)

    else:

        cols = st.columns(4)

        with cols[0]:
            metric("READINESS SCORE", "Not assessed",
                   "Take the assessment first")

        with cols[1]:
            metric("RESUME MATCH", "—",
                   "Resume module not implemented", "teal")

        with cols[2]:
            metric("SKILL GAPS", "—",
                   "Available after assessment", "red")

        with cols[3]:
            metric("MOCK INTERVIEWS", "—",
                   "Module planned")

        st.info(
            "You haven't completed your technical assessment yet. "
            "Take the assessment to generate your placement readiness report."
        )

        if st.button("Start Student Assessment", type="primary"):
            st.session_state.page = "Student Assessment"
            st.rerun()

    st.write("")

    st.markdown(
        """
        <div class="panel">
            <div class="panel-title">Other modules</div>
            <div class="panel-sub">
                These features are planned for future development.
                They are not currently active.
            </div>
            <br>
            Resume Analyzer · Mock Interviews · Learning Roadmap · Placement Drives
        </div>
        """,
        unsafe_allow_html=True
    )


# --------------------------------------------------
# 7. STUDENT ASSESSMENT
# --------------------------------------------------

def assessment():

    st.markdown(
        """
        <div class="crumb">Home / Student Assessment</div>
        <div class="heading">Student Assessment</div>
        <div class="subheading">
            Evaluate your technical readiness across core computer-science domains.
        </div>
        <br>
        """,
        unsafe_allow_html=True
    )

    c1, c2, c3 = st.columns(3)

    name = c1.text_input(
        "Student name",
        value=st.session_state.student
    )

    company = c2.selectbox(
        "Target company",
        list(COMPANIES.keys()),
        index=list(COMPANIES.keys()).index(st.session_state.company)
    )

    roles = list(COMPANIES[company].keys())

    role = c3.selectbox(
        "Target role",
        roles,
        index=roles.index(st.session_state.role)
        if st.session_state.role in roles else 0
    )

    st.info(
        f"{len(QUESTIONS)} MCQs · {len(DOMAINS)} domains · "
        "1 mark each · No negative marking"
    )

    attempt = st.session_state.attempt

    with st.form(key=f"assessment_form_{attempt}"):

        for domain in DOMAINS:

            st.markdown(f"### {domain}")

            domain_questions = [
                q for q in QUESTIONS
                if q["domain"] == domain
            ]

            for q in domain_questions:

                st.markdown(
                    f"**{q['id']}. [{q['difficulty']}] {q['question']}**"
                )

                options = ["— Select an answer —"] + q["options"]

                st.selectbox(
                    "Choose one",
                    options,
                    index=0,
                    key=f"answer_{attempt}_{q['id']}",
                    label_visibility="collapsed"
                )

        submitted = st.form_submit_button(
            "Submit Assessment",
            type="primary",
            use_container_width=True
        )

    if submitted:

        answers = {}

        for q in QUESTIONS:

            selected = st.session_state.get(
                f"answer_{attempt}_{q['id']}",
                "— Select an answer —"
            )

            answers[q["id"]] = selected

        st.session_state.answers = answers
        st.session_state.student = name.strip() or "Student"
        st.session_state.company = company
        st.session_state.role = role
        st.session_state.submitted = True

        score, percentage, rows = calculate_results(answers)

        st.success("Assessment submitted successfully!")

        st.subheader("Your assessment result")

        a, b, c = st.columns(3)

        a.metric("Total score", f"{score}/{len(QUESTIONS)}")
        b.metric("Percentage", f"{percentage}%")
        c.metric("Domains", len(DOMAINS))

        st.markdown("### Domain-wise performance")

        st.dataframe(
            pd.DataFrame(rows),
            use_container_width=True,
            hide_index=True
        )

        st.info("Visit Skill Gap to view your detailed analysis.")


# --------------------------------------------------
# 8. SKILL GAP ANALYSIS
# --------------------------------------------------

def skill_gap():

    st.markdown(
        """
        <div class="crumb">Home / Skill Gap</div>
        <div class="heading">Skill Gap Analysis</div>
        <div class="subheading">
            Compare your assessment performance with your selected company role.
        </div>
        <br>
        """,
        unsafe_allow_html=True
    )

    if not st.session_state.submitted:

        st.warning(
            "Complete the Student Assessment first to generate your personal report."
        )
        return

    score, percentage, rows = calculate_results(
        st.session_state.answers
    )

    a, b, c = st.columns(3)

    a.metric("Readiness score", f"{percentage}/100")
    b.metric("Correct answers", f"{score}/{len(QUESTIONS)}")
    c.metric("Domains assessed", len(DOMAINS))

    df = pd.DataFrame(rows)

    st.markdown("### Domain-wise performance")

    st.bar_chart(
        df.set_index("Domain")["Score"],
        color="#2dd4bf"
    )

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    requirements = COMPANIES[
        st.session_state.company
    ][st.session_state.role]

    gaps = []

    for row in rows:

        target = requirements["domain_targets"].get(
            row["Domain"], 60
        )

        gap = max(round(target - row["Score"], 1), 0)

        if gap >= 20:
            priority = "High"
        elif gap > 0:
            priority = "Improve"
        else:
            priority = "On track"

        gaps.append({
            "Domain": row["Domain"],
            "Your score": row["Score"],
            "Illustrative role target": target,
            "Gap": gap,
            "Priority": priority
        })

    st.markdown(
        f"### {st.session_state.company} — {st.session_state.role}"
    )

    st.dataframe(
        pd.DataFrame(gaps),
        use_container_width=True,
        hide_index=True
    )

    st.caption(
        "Company thresholds are illustrative project data, "
        "not official hiring criteria. Assessment scoring is deterministic."
    )

    if st.button("Retake Assessment", type="primary"):

        st.session_state.submitted = False
        st.session_state.answers = {}
        st.session_state.attempt += 1
        st.session_state.page = "Student Assessment"

        st.rerun()


# --------------------------------------------------
# 9. PLANNED MODULES
# --------------------------------------------------

def planned_page(title, description):

    st.markdown(
        f"""
        <div class="crumb">Home / {title}</div>
        <div class="heading">{title}</div>
        <div class="subheading">{description}</div>
        <br>
        """,
        unsafe_allow_html=True
    )

    st.info(
        f"{title} is planned for a later development milestone. "
        "This module is not yet implemented in the current review prototype."
    )


# --------------------------------------------------
# 10. SIDEBAR NAVIGATION
# --------------------------------------------------

if "page" not in st.session_state:
    st.session_state.page = "Dashboard"

NAV_ITEMS = [
    "Dashboard",
    "Student Assessment",
    "Skill Gap",
    "Resume Analyzer",
    "Mock Interviews",
    "Learning Roadmap",
    "Placement Drives",
    "Settings"
]

with st.sidebar:

    st.markdown(
        """
        <div class="brand">
            <div class="brand-icon">PP</div>
            <div>
                <div class="brand-name">PrepPath</div>
                <div class="brand-sub">Placement Readiness</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.caption("WORKSPACE")

    selected_page = st.radio(
        "Navigation",
        NAV_ITEMS,
        index=NAV_ITEMS.index(st.session_state.page),
        label_visibility="collapsed"
    )

    st.session_state.page = selected_page

    st.markdown("---")

    st.markdown(
        f"""
        **{st.session_state.student}**

        B.Tech CSE · Final Year
        """
    )


# --------------------------------------------------
# 11. PAGE ROUTING
# --------------------------------------------------

page = st.session_state.page

if page == "Dashboard":

    dashboard()

elif page == "Student Assessment":

    assessment()

elif page == "Skill Gap":

    skill_gap()

elif page == "Resume Analyzer":

    planned_page(
        "Resume Analyzer",
        "Upload your resume and compare extracted skills with target roles."
    )

elif page == "Mock Interviews":

    planned_page(
        "Mock Interviews",
        "Practice technical and behavioral interviews."
    )

elif page == "Learning Roadmap":

    planned_page(
        "Learning Roadmap",
        "Follow a personalized sequence of skills and preparation tasks."
    )

elif page == "Placement Drives":

    planned_page(
        "Placement Drives",
        "Explore relevant opportunities and track application deadlines."
    )

elif page == "Settings":

    planned_page(
        "Settings",
        "Manage your student profile and preferences."
    )


# --------------------------------------------------
# 12. FOOTER
# --------------------------------------------------

st.markdown(
    """
    <div style="
        text-align:center;
        color:#667286;
        font-size:10px;
        padding:24px 0;
    ">
        PrepPath · CareerPilot Placement Readiness Agent · Review Prototype
    </div>
    """,
    unsafe_allow_html=True
)
```
