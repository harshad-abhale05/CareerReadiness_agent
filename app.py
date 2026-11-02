import json
from pathlib import Path
import pandas as pd
import streamlit as st

ROOT = Path(__file__).parent
with open(ROOT / 'data' / 'questions.json', encoding='utf-8') as f:
    QUESTIONS = json.load(f)
with open(ROOT / 'data' / 'company_requirements.json', encoding='utf-8') as f:
    COMPANIES = json.load(f)

st.set_page_config(page_title='CareerPilot | Placement Readiness', page_icon='🎓', layout='wide')
st.markdown('''
<style>
.stApp {background:linear-gradient(135deg,#f4f7ff 0%,#f8faff 55%,#f2f5ff 100%); color:#17213b;}
[data-testid="stHeader"] {background:rgba(244,247,255,.88);}
.block-container {padding-top:1.45rem; padding-bottom:2rem; max-width:1450px;}
section[data-testid="stSidebar"] {background:linear-gradient(180deg,#17213f 0%,#101a35 100%); border-right:1px solid #26365e;}
section[data-testid="stSidebar"] * {color:#f4f7ff !important;}
.brand {text-align:center;padding:14px 6px 24px;margin-bottom:16px;border-bottom:1px solid rgba(255,255,255,.13);}
.brand-icon {font-size:2.7rem;}.brand-name {font-size:1.55rem;font-weight:800;}.brand-sub {color:#bdc9e8!important;font-size:.83rem;}
.welcome {background:linear-gradient(110deg,#e6edff,#f4edff);border:1px solid #dce5ff;border-radius:20px;padding:23px 26px;margin-bottom:18px;}
.welcome h1 {color:#142044;font-size:2rem;margin:0;}.welcome p {color:#53617f;margin:.35rem 0 0;}
.metric-card {border:1px solid #e0e7fb;border-radius:17px;padding:17px 18px;min-height:130px;box-shadow:0 5px 18px rgba(45,65,120,.05);}
.metric-label {color:#52617f;font-size:.82rem;letter-spacing:.04em;}.metric-value {color:#17213b;font-size:2rem;font-weight:800;margin-top:5px;}.metric-help {color:#64748b;font-size:.8rem;margin-top:3px;}
.card {background:rgba(255,255,255,.94);border:1px solid #e2e8f5;border-radius:18px;padding:20px 22px;margin-bottom:16px;box-shadow:0 5px 20px rgba(45,65,120,.045);}
.card h3 {color:#17213b;margin:0 0 5px;font-size:1.12rem;}.muted {color:#64748b;font-size:.88rem;}
.pill {display:inline-block;border-radius:30px;padding:5px 11px;background:#e9efff;color:#315eea;font-size:.78rem;font-weight:700;}
div.stButton>button[kind="primary"] {background:linear-gradient(90deg,#315eea,#694be8);border:0;border-radius:10px;color:white;}
div[data-testid="stMetric"] {background:white;border:1px solid #e2e8f5;padding:14px;border-radius:14px;box-shadow:0 4px 14px rgba(45,65,120,.04);}
</style>
''', unsafe_allow_html=True)

if 'answers' not in st.session_state: st.session_state.answers = {}
if 'submitted' not in st.session_state: st.session_state.submitted = False
if 'student' not in st.session_state: st.session_state.student = 'Demo Student'
if 'company' not in st.session_state: st.session_state.company = list(COMPANIES)[0]
if 'role' not in st.session_state: st.session_state.role = list(COMPANIES[st.session_state.company])[0]
domains = list(dict.fromkeys(q['domain'] for q in QUESTIONS))

with st.sidebar:
    st.markdown('''<div class="brand"><div class="brand-icon">🎓</div><div class="brand-name">CareerPilot</div><div class="brand-sub">Placement Readiness Agent</div></div>''', unsafe_allow_html=True)
    page = st.radio('Navigation', ['Dashboard','Student Assessment','Results & Skill Gaps','Panel Members'], label_visibility='collapsed')
    st.markdown('---')
    st.caption('Built for student career readiness')
    st.markdown(f"<div style='padding:10px 4px;color:#dbe5ff!important'>👤 {st.session_state.student}<br><span style='font-size:.78rem;color:#aebde0!important'>B.Tech CSE · Final Year</span></div>", unsafe_allow_html=True)

def calculate_report(answers):
    total = len(QUESTIONS)
    score = sum(1 for q in QUESTIONS if answers.get(q['id']) == q['correct_answer'])
    pct = score / total * 100 if total else 0
    rows = []
    for domain in domains:
        qs = [q for q in QUESTIONS if q['domain'] == domain]
        correct = sum(1 for q in qs if answers.get(q['id']) == q['correct_answer'])
        rows.append({'Domain':domain,'Score':round(correct/len(qs)*100,1),'Correct':f'{correct}/{len(qs)}'})
    return score, pct, rows

def dashboard():
    st.markdown(f'<div class="welcome"><h1>Welcome back, {st.session_state.student}!</h1><p>Here is where your placement readiness stands today. Build your skills, measure your progress, and prepare with direction.</p></div>', unsafe_allow_html=True)
    if st.session_state.submitted:
        score,pct,rows = calculate_report(st.session_state.answers)
        gap_count = sum(1 for r in rows if r['Score'] < 60)
        cards = [('READINESS SCORE',f'{pct:.0f}/100',f'{score}/{len(QUESTIONS)} questions correct','linear-gradient(120deg,#e3ecff,#d9e5ff)'),('RESUME MATCH','—','Resume analysis is a planned module','linear-gradient(120deg,#ddf8f2,#d4f3ee)'),('SKILL GAPS',str(gap_count),'Domains below the 60% practice benchmark','linear-gradient(120deg,#fff0f2,#ffe3eb)')]
    else:
        rows=[]
        cards=[('READINESS SCORE','—','Complete the assessment to calculate','linear-gradient(120deg,#e3ecff,#d9e5ff)'),('RESUME MATCH','—','Resume analysis is a planned module','linear-gradient(120deg,#ddf8f2,#d4f3ee)'),('SKILL GAPS','—','Complete an assessment to identify gaps','linear-gradient(120deg,#fff0f2,#ffe3eb)')]
    cols=st.columns(3)
    for col,(label,value,help_text,bg) in zip(cols,cards):
        with col: st.markdown(f'<div class="metric-card" style="background:{bg}"><div class="metric-label">{label}</div><div class="metric-value">{value}</div><div class="metric-help">{help_text}</div></div>',unsafe_allow_html=True)
    left,right=st.columns([1.55,1])
    with left:
        st.markdown('<div class="card"><h3>📊 Skill readiness overview</h3><div class="muted">Your assessed strengths and improvement areas</div></div>',unsafe_allow_html=True)
        if rows:
            df=pd.DataFrame(rows); st.bar_chart(df.set_index('Domain')['Score'],height=270,color='#4267e8'); st.dataframe(df,use_container_width=True,hide_index=True)
        else: st.info('Your domain-wise skill chart will appear here after you complete the 40-question assessment.')
    with right:
        st.markdown('<div class="card"><h3>🧭 Your next steps</h3><div class="muted">A focused path to placement readiness</div><br><span class="pill">Start here</span><br><br><b>1. Complete technical assessment</b><br><span class="muted">Evaluate eight core computer-science domains.</span><br><br><b>2. Review skill gaps</b><br><span class="muted">Compare your scores with a selected company-role profile.</span><br><br><b>3. Follow recommendations</b><br><span class="muted">Prioritize weaker domains and retake assessments.</span></div><div class="card"><h3>🚀 Project modules</h3><div class="muted">Current review build</div><br>✅ Student assessment<br>✅ Automatic evaluation<br>✅ Skill-gap comparison<br>🛠 Resume analysis — planned<br>🛠 Mock interviews — planned<br>🛠 Progress tracking — planned</div>',unsafe_allow_html=True)

def assessment():
    st.markdown('<div class="welcome"><h1>Student Assessment</h1><p>Evaluate your technical readiness across eight core CS domains.</p></div>',unsafe_allow_html=True)
    c1,c2,c3=st.columns(3)
    student=c1.text_input('Student name',value=st.session_state.student)
    company=c2.selectbox('Target company',list(COMPANIES),index=list(COMPANIES).index(st.session_state.company))
    roles=list(COMPANIES[company]); role=c3.selectbox('Target role',roles,index=roles.index(st.session_state.role) if st.session_state.role in roles else 0)
    st.info(f'Review assessment: {len(QUESTIONS)} MCQs · 8 domains · 1 mark each · No negative marking.')
    with st.form('assessment_form'):
        for domain in domains:
            st.markdown(f'### {domain}')
            for q in [x for x in QUESTIONS if x['domain']==domain]:
                st.markdown(f"**{q['id']}. [{q['difficulty']}] {q['question']}**")
                opts=['— Select an answer —']+q['options']; old=st.session_state.answers.get(q['id'],'— Select an answer —')
                st.selectbox('Choose one',opts,index=opts.index(old) if old in opts else 0,key=f"ans_{q['id']}",label_visibility='collapsed')
        submitted=st.form_submit_button('Submit assessment',type='primary',use_container_width=True)
    if submitted:
        st.session_state.answers={q['id']:st.session_state.get(f"ans_{q['id']}",'— Select an answer —') for q in QUESTIONS}
        st.session_state.submitted=True; st.session_state.student=student.strip() or 'Student'; st.session_state.company=company; st.session_state.role=role
        st.success('Assessment submitted. Open Results & Skill Gaps to view your report.')

def results():
    st.markdown('<div class="welcome"><h1>Results & Skill Gaps</h1><p>Understand your performance against your selected company-role profile.</p></div>',unsafe_allow_html=True)
    if not st.session_state.submitted:
        st.warning('No assessment has been submitted in this session yet.')
        if st.button('Load sample result for project demonstration'):
            st.session_state.answers={q['id']:(q['correct_answer'] if i%3 else q['options'][0]) for i,q in enumerate(QUESTIONS)}
            st.session_state.submitted=True; st.session_state.student='Demo Student'; st.rerun()
        return
    score,pct,rows=calculate_report(st.session_state.answers)
    st.markdown(f"**Student:** {st.session_state.student} &nbsp; · &nbsp; **Target:** {st.session_state.company} — {st.session_state.role}")
    a,b,c=st.columns(3); a.metric('Readiness score',f'{pct:.1f}/100'); b.metric('Correct answers',f'{score}/{len(QUESTIONS)}'); c.metric('Domains assessed',len(domains))
    df=pd.DataFrame(rows); st.markdown('<div class="card"><h3>Domain-wise performance</h3><div class="muted">Scores are calculated from submitted answers.</div></div>',unsafe_allow_html=True)
    st.bar_chart(df.set_index('Domain')['Score'],color='#4267e8'); st.dataframe(df,use_container_width=True,hide_index=True)
    req=COMPANIES[st.session_state.company][st.session_state.role]; gap_rows=[]
    for row in rows:
        target=req['domain_targets'].get(row['Domain'],60); diff=round(target-row['Score'],1)
        gap_rows.append({'Domain':row['Domain'],'Student score':row['Score'],'Illustrative target':target,'Gap':max(diff,0),'Status':'Priority' if diff>=20 else ('Improve' if diff>0 else 'On track')})
    gap_df=pd.DataFrame(gap_rows); st.markdown(f"### Comparison with {st.session_state.company} role profile"); st.dataframe(gap_df,use_container_width=True,hide_index=True)
    priorities=gap_df[gap_df['Gap']>0].sort_values('Gap',ascending=False); st.markdown('### CareerPilot recommendations')
    if priorities.empty: st.success('Your scores meet or exceed this illustrative profile’s domain thresholds. Continue with advanced practice.')
    else:
        for _,r in priorities.head(5).iterrows(): st.write(f"**{r['Domain']} — {r['Status']}**: Current {r['Student score']}%, illustrative target {r['Illustrative target']}%. Prioritize focused practice, then retake a fresh assessment.")
    st.caption('Scoring and gap calculations are deterministic and explainable. Recommendations in this review MVP are rule-generated; LLM-based agent orchestration is planned.')

def panel_members():
    st.markdown('<div class="welcome"><h1>Panel Members</h1><p>Technical overview for project evaluation — architecture, API design, and implementation status.</p></div>',unsafe_allow_html=True)
    st.info('The API technical design is kept in this panel-only section and in the source code, not in the student dashboard.')
    st.markdown('### System architecture')
    st.code('''Student\n  |\n  v\nCareerPilot Web UI\n  |\n  +--> Assessment Module --> Question Bank --> Evaluation Engine\n  |\n  +--> Company/Role Selector --> Company Requirements API --> Requirements JSON / DB (future)\n  |\n  v\nCareer Readiness Orchestrator (planned AI agent)\n  |\n  +--> Skill Gap Analysis Tool\n  +--> Recommendation Tool\n  +--> Progress Tracking Tool (planned)\n  |\n  v\nPersonalized Career Readiness Report''',language='text')
    st.markdown('### API design for technical review')
    st.code('''GET /api/companies\nGET /api/companies/{company}/roles\nGET /api/requirements?company=Google&role=Software%20Development%20Engineer\n\nExample JSON response:\n{\n  "company": "Google",\n  "role": "Software Development Engineer",\n  "domain_targets": {\n    "Data Structures & Algorithms": 85,\n    "Operating Systems": 70,\n    "DBMS": 70\n  }\n}''',language='text')
    st.success('Implemented: 40-question bank, assessment UI, deterministic scoring, domain-wise report, company-role JSON profiles, rule-based skill-gap analysis.')
    st.warning('Planned: production REST API endpoints, database persistence, verified live job-description ingestion, LLM/LangGraph tool orchestration, coding sandbox, authentication and progress tracking.')
    st.caption('Company profiles are illustrative project data, not official company APIs or guaranteed hiring criteria.')

if page=='Dashboard': dashboard()
elif page=='Student Assessment': assessment()
elif page=='Results & Skill Gaps': results()
else: panel_members()
st.markdown('<div style="text-align:center;color:#8792aa;font-size:.78rem;padding:20px 0">CareerPilot · Placement Readiness Agent · Review prototype</div>',unsafe_allow_html=True)
