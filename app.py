import json
from pathlib import Path
import streamlit as st
import pandas as pd

ROOT = Path(__file__).parent
with open(ROOT / "data" / "questions.json", encoding="utf-8") as f:
    QUESTIONS = json.load(f)
with open(ROOT / "data" / "company_requirements.json", encoding="utf-8") as f:
    COMPANIES = json.load(f)

st.set_page_config(page_title="CareerPilot | Placement Readiness", page_icon="🎯", layout="wide")
st.markdown("""
<style>
.block-container {padding-top: 1.7rem; max-width: 1180px;}
.hero {padding: 1.35rem 1.6rem; border-radius: 16px; background: linear-gradient(115deg,#10233f,#245b82); color:white; margin-bottom:1rem;}
.hero h1 {color:white; margin:0; font-size:2.1rem;}
.hero p {color:#dceaf5; margin:.35rem 0 0 0;}
.small-note {font-size:.88rem; color:#6b7280;}
div[data-testid="stMetric"] {background:#f5f8fc; padding:14px; border-radius:12px;}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="hero"><h1>🎯 CareerPilot</h1><p>AI-powered career and placement readiness — review MVP</p></div>', unsafe_allow_html=True)
st.caption("Prototype build: assessment → evaluation → company-role comparison → personalized recommendations.")

tab1, tab2, tab3, tab4 = st.tabs(["Student Assessment", "Results & Skill Gaps", "Company Requirements API", "Project Architecture"])

domains = list(dict.fromkeys(q["domain"] for q in QUESTIONS))
with tab1:
    st.subheader("Student assessment")
    c1,c2,c3 = st.columns(3)
    student = c1.text_input("Student name", value="Demo Student")
    company = c2.selectbox("Target company", list(COMPANIES.keys()))
    role = c3.selectbox("Target role", list(COMPANIES[company].keys()))
    st.info("For this review prototype, the assessment contains 40 MCQs (5 per domain). Each question carries 1 mark. No negative marking.")
    if "answers" not in st.session_state: st.session_state.answers = {}
    if "submitted" not in st.session_state: st.session_state.submitted = False
    with st.form("assessment_form"):
        for domain in domains:
            st.markdown(f"### {domain}")
            for q in [x for x in QUESTIONS if x["domain"] == domain]:
                st.markdown(f"**{q['id']}. [{q['difficulty']}] {q['question']}**")
                default = st.session_state.answers.get(q["id"], "— Select an answer —")
                opts = ["— Select an answer —"] + q["options"]
                ix = opts.index(default) if default in opts else 0
                st.selectbox("Choose one", opts, index=ix, key=f"ans_{q['id']}", label_visibility="collapsed")
        submitted = st.form_submit_button("Submit assessment", type="primary", use_container_width=True)
    if submitted:
        st.session_state.answers = {q["id"]: st.session_state.get(f"ans_{q['id']}", "— Select an answer —") for q in QUESTIONS}
        st.session_state.submitted = True
        st.session_state.student = student
        st.session_state.company = company
        st.session_state.role = role
        st.success("Assessment submitted. Open the Results & Skill Gaps tab.")
with tab2:
    st.subheader("Evaluation and skill-gap report")
    if not st.session_state.get("submitted"):
        st.warning("Submit the assessment first. You can use the preloaded demo result below to inspect the reporting logic.")
        demo = st.button("Load demo assessment result")
    else: demo = False
    if st.session_state.get("submitted") or demo:
        if demo:
            ans = {q["id"]: q["correct_answer"] if i % 3 != 0 else q["options"][0] for i,q in enumerate(QUESTIONS)}
            target_company, target_role, name = "Google", "Software Development Engineer", "Demo Student"
        else:
            ans = st.session_state.answers
            target_company, target_role, name = st.session_state.company, st.session_state.role, st.session_state.student
        total = len(QUESTIONS)
        score = sum(1 for q in QUESTIONS if ans.get(q["id"]) == q["correct_answer"])
        pct = score / total * 100
        st.markdown(f"**Student:** {name} &nbsp; | &nbsp; **Target:** {target_company} — {target_role}")
        a,b,c = st.columns(3)
        a.metric("Overall score", f"{pct:.1f}%")
        b.metric("Correct answers", f"{score}/{total}")
        b2 = sum(1 for q in QUESTIONS if q["difficulty"] == "Beginner" and ans.get(q["id"]) == q["correct_answer"])
        c.metric("Questions assessed", total)
        rows=[]
        for d in domains:
            dq=[q for q in QUESTIONS if q["domain"]==d]
            got=sum(1 for q in dq if ans.get(q["id"])==q["correct_answer"])
            rows.append({"Domain":d,"Score":round(got/len(dq)*100,1),"Correct":f"{got}/{len(dq)}"})
        df=pd.DataFrame(rows)
        st.markdown("#### Domain-wise performance")
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.bar_chart(df.set_index("Domain")["Score"])
        req=COMPANIES[target_company][target_role]
        gap=[]
        for r in rows:
            target=req["domain_targets"].get(r["Domain"],60)
            delta=round(target-r["Score"],1)
            gap.append({"Domain":r["Domain"],"Student score":r["Score"],"Illustrative target":target,"Gap":max(delta,0),"Status":"Priority" if delta>=20 else ("Improve" if delta>0 else "On track")})
        gdf=pd.DataFrame(gap)
        st.markdown(f"#### Comparison with {target_company} role profile")
        st.dataframe(gdf, use_container_width=True, hide_index=True)
        priorities=gdf[gdf["Gap"]>0].sort_values("Gap",ascending=False)
        st.markdown("#### CareerPilot agent recommendations")
        if priorities.empty:
            st.success("The assessed domains meet or exceed the illustrative profile thresholds. Continue with advanced practice and role-specific preparation.")
        else:
            for _,r in priorities.head(4).iterrows():
                st.write(f"**{r['Domain']} — {r['Status']}**: Current {r['Student score']}%, illustrative target {r['Illustrative target']}%. Prioritize focused practice, then retake a fresh assessment.")
        st.caption("Scoring and threshold comparison are deterministic and explainable. Recommendations are rule-generated in this MVP; LLM-based agent reasoning and adaptive planning are planned integration work.")
with tab3:
    st.subheader("Company requirements API")
    st.write("Select a company and role to inspect the structured response that the backend API will expose.")
    co=st.selectbox("Company",list(COMPANIES.keys()),key="api_company")
    ro=st.selectbox("Role",list(COMPANIES[co].keys()),key="api_role")
    record=COMPANIES[co][ro]
    payload={"company":co,"role":ro,**record}
    st.json(payload, expanded=True)
    st.download_button("Download API response (JSON)",json.dumps(payload,indent=2),file_name=f"{co.lower()}_{ro.lower().replace(' ','_')}_requirements.json",mime="application/json")
    st.caption("This is a prototype requirements dataset, not an official company API or a guarantee of universal hiring criteria. Profiles must be validated against current job postings.")
with tab4:
    st.subheader("System architecture")
    st.code("""Student
  |
  v
CareerPilot Web UI
  |
  +--> Assessment Module --> Question Bank --> Evaluation Engine
  |
  +--> Company/Role Selector --> Company Requirements API --> Requirements DB
  |
  v
Career Readiness Orchestrator (AI Agent)
  |
  +--> Skill Gap Analysis Tool
  +--> Recommendation Tool
  +--> Progress Tracking Tool (next phase)
  |
  v
Personalized Career Readiness Report""", language="text")
    st.markdown("**Implemented in this review MVP:** question bank, assessment UI, deterministic scoring, domain report, company/role JSON profiles, rule-based gap analysis and recommendations.")
    st.markdown("**Next development:** persistent student accounts/results, coding-question execution in a sandbox, live job-description ingestion, verified role profiles, LLM/LangGraph tool orchestration, progress tracking and production deployment.")
    st.warning("The current assessment is a review prototype with 40 MCQs. It is not a validated psychometric or hiring test.")
st.divider()
st.caption("CareerPilot • Final-year project progress prototype")
