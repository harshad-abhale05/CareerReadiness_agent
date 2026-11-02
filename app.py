import json
from pathlib import Path
import pandas as pd
import streamlit as st

ROOT = Path(__file__).parent
with open(ROOT / 'data' / 'questions.json', encoding='utf-8') as f:
    QUESTIONS = json.load(f)
with open(ROOT / 'data' / 'company_requirements.json', encoding='utf-8') as f:
    COMPANIES = json.load(f)

# Demo data is kept separate from UI code. Replace this object with API data later.
DASHBOARD_DATA = {
    'student': {'name': 'Harshad Abhale', 'degree': 'B.Tech CSE · Final Year'},
    'stats': {'readiness': 78, 'readiness_change': '+6 since last week', 'resume_match': 82,
              'skill_gaps': 4, 'high_priority': 2, 'mock_count': 11, 'mock_average': 7.4},
    'skills': [
        {'name': 'Data Structures & Algorithms', 'score': 88, 'color': 'teal'},
        {'name': 'System Design', 'score': 54, 'color': 'gold'},
        {'name': 'Cloud & Deployment (AWS)', 'score': 71, 'color': 'teal'},
        {'name': 'Behavioral / Communication', 'score': 39, 'color': 'red'},
    ],
    'roles': [
        {'code': 'TCS', 'role': 'Software Engineer — TCS Digital', 'details': '₹7.5L avg CTC · 90% skill match', 'badge': 'Apply', 'type': 'good'},
        {'code': 'INF', 'role': 'Backend Developer — Infosys', 'details': '₹8.2L avg CTC · 84% skill match', 'badge': 'Apply', 'type': 'good'},
        {'code': 'AMZ', 'role': 'SDE Intern — Amazon', 'details': '₹1.1L/mo stipend · 76% skill match', 'badge': '2 days left', 'type': 'warning'},
    ],
    'interview': {'score': 76, 'last': 'Backend round, DSA + HR',
                  'feedback': 'Strong on problem-solving clarity. Work on concise answers under time pressure.'},
    'drives': [
        {'code': 'GO', 'name': 'Google — SWE Intern', 'applied': '45 applied', 'deadline': '2d left', 'type': 'warning'},
        {'code': 'MS', 'name': 'Microsoft — Data Analyst', 'applied': '38 applied', 'deadline': '5d left', 'type': 'good'},
    ],
}

st.set_page_config(page_title='PrepPath | Placement Readiness', page_icon='🎓', layout='wide', initial_sidebar_state='expanded')

st.markdown(r'''<style>
:root{--bg:#0b0e14;--side:#10141d;--card:#121720;--border:#252d3a;--text:#edf1f8;--muted:#8995a8;--gold:#f5bd35;--teal:#2dd4bf;--red:#fa7567;--purple:#9b8cff}
.stApp{background:var(--bg);color:var(--text)} [data-testid="stHeader"]{background:rgba(11,14,20,.96)}
.block-container{max-width:1500px;padding-top:1.6rem;padding-bottom:2rem}
section[data-testid="stSidebar"]{background:var(--side);border-right:1px solid var(--border)}
section[data-testid="stSidebar"]>div{padding-top:1.2rem} section[data-testid="stSidebar"] *{color:var(--text)}
.brand{display:flex;align-items:center;gap:11px;padding:8px 5px 27px}
.brand-icon{width:39px;height:39px;border-radius:10px;background:var(--gold);color:#15120a!important;display:flex;align-items:center;justify-content:center;font-weight:900}
.brand-name{font-size:17px;font-weight:800}.brand-sub{font-size:11px;color:var(--muted)!important;margin-top:3px}
.userbox{display:flex;align-items:center;gap:10px;border:1px solid var(--border);background:#171d29;border-radius:11px;padding:11px;margin-top:22px}
.avatar{width:35px;height:35px;border-radius:50%;background:#7564d9;display:flex;align-items:center;justify-content:center;font-weight:800}
.user-name{font-size:12px;font-weight:700}.user-degree{font-size:10px;color:var(--muted)!important;margin-top:3px}
.crumb{font-size:12px;color:var(--muted);margin-bottom:7px}.heading{font-size:27px;font-weight:800;color:#f1f4fa}.subheading{font-size:13px;color:var(--muted);margin-top:5px}
.metric{background:var(--card);border:1px solid var(--border);border-left:3px solid var(--gold);border-radius:12px;padding:15px 16px;min-height:112px}
.metric.teal{border-left-color:var(--teal)}.metric.red{border-left-color:var(--red)}.metric.purple{border-left-color:var(--purple)}
.metric-label{font-size:10px;letter-spacing:.7px;color:var(--muted)}.metric-value{font-size:27px;font-weight:800;margin-top:8px}.metric-help{font-size:11px;color:var(--muted);margin-top:4px}
.panel{background:var(--card);border:1px solid var(--border);border-radius:13px;padding:18px;margin-bottom:15px}
.panel-title{font-size:15px;font-weight:750;color:#f1f4f9}.panel-sub{font-size:11px;color:var(--muted);margin-top:4px}
.skill{margin-top:17px}.skill-head{display:flex;justify-content:space-between;font-size:12px;margin-bottom:7px}.track{height:6px;background:#252d3a;border-radius:20px;overflow:hidden}.fill{height:100%;border-radius:20px}.fill.teal{background:var(--teal)}.fill.gold{background:var(--gold)}.fill.red{background:var(--red)}
.item{display:flex;align-items:center;gap:11px;padding:13px 0;border-bottom:1px solid var(--border)}.item:last-child{border:0;padding-bottom:0}
.logo{width:35px;height:35px;flex-shrink:0;border-radius:9px;background:#1c2432;color:var(--gold);display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:800}
.item-main{flex:1;min-width:0}.item-title{font-size:12px;font-weight:700}.item-detail{font-size:10px;color:var(--muted);margin-top:4px}
.badge{padding:5px 9px;border-radius:20px;font-size:10px;font-weight:700;white-space:nowrap}.badge.good{color:var(--teal);background:#12312f}.badge.warning{color:var(--red);background:#382321}
.ring{width:78px;height:78px;border-radius:50%;background:conic-gradient(var(--teal) 0 76%,#27313d 76% 100%);display:flex;align-items:center;justify-content:center;flex-shrink:0}.ring-inner{width:62px;height:62px;border-radius:50%;background:var(--card);display:flex;align-items:center;justify-content:center;font-size:17px;font-weight:800}
.interview{display:flex;align-items:center;gap:15px;margin:17px 0 14px}.feedback{font-size:11px;line-height:1.55;color:#b4bfce}
.quick{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-top:13px}.quick div{background:#171e29;border:1px solid var(--border);border-radius:10px;padding:13px 5px;text-align:center;font-size:10px;transition:.2s}.quick div:hover{background:#222b39;border-color:var(--gold);transform:translateY(-2px)}.quick span{display:block;font-size:18px;margin-bottom:7px}
div.stButton>button{background:#171e29;color:#e9eef7;border:1px solid #303949;border-radius:8px;font-size:12px;transition:.2s}
div.stButton>button:hover{border-color:var(--gold);color:var(--gold);background:#202938}
div.stButton>button[kind="primary"]{background:var(--gold);color:#15120a;border:1px solid var(--gold);font-weight:800}
div.stButton>button[kind="primary"]:hover{background:#ffd15c;color:#15120a}
[data-testid="stMetric"]{background:var(--card);border:1px solid var(--border);border-radius:11px;padding:12px}
.stTextInput input,.stSelectbox div[data-baseweb="select"]>div{background:#151b25;color:var(--text);border-color:#303949}
@media(max-width:900px){.block-container{padding-left:1rem;padding-right:1rem}.heading{font-size:22px}}
</style>''', unsafe_allow_html=True)

if 'answers' not in st.session_state: st.session_state.answers = {}
if 'submitted' not in st.session_state: st.session_state.submitted = False
if 'student' not in st.session_state: st.session_state.student = DASHBOARD_DATA['student']['name']
if 'company' not in st.session_state: st.session_state.company = list(COMPANIES)[0]
if 'role' not in st.session_state: st.session_state.role = list(COMPANIES[st.session_state.company])[0]
domains = list(dict.fromkeys(q['domain'] for q in QUESTIONS))

with st.sidebar:
    st.markdown('<div class="brand"><div class="brand-icon">PP</div><div><div class="brand-name">PrepPath</div><div class="brand-sub">Placement Readiness</div></div></div>', unsafe_allow_html=True)
    st.caption('WORKSPACE')
    page = st.radio('Navigation', ['Dashboard','Resume Analyzer','Skill Gap','Mock Interviews','Learning Roadmap','Placement Drives','Settings'], label_visibility='collapsed')
    st.markdown(f'<div class="userbox"><div class="avatar">HA</div><div><div class="user-name">{DASHBOARD_DATA["student"]["name"]}</div><div class="user-degree">{DASHBOARD_DATA["student"]["degree"]}</div></div></div>', unsafe_allow_html=True)
    st.caption('⚙ Settings')

def report(answers):
    total=len(QUESTIONS); score=sum(1 for q in QUESTIONS if answers.get(q['id'])==q['correct_answer'])
    rows=[]
    for domain in domains:
        qs=[q for q in QUESTIONS if q['domain']==domain]
        correct=sum(1 for q in qs if answers.get(q['id'])==q['correct_answer'])
        rows.append({'Domain':domain,'Score':round(correct/len(qs)*100,1),'Correct':f'{correct}/{len(qs)}'})
    return score, score/total*100 if total else 0, rows

def metric(label,value,help_text,accent=''):
    st.markdown(f'<div class="metric {accent}"><div class="metric-label">{label}</div><div class="metric-value">{value}</div><div class="metric-help">{help_text}</div></div>',unsafe_allow_html=True)

def dashboard():
    a,b=st.columns([3,1.15])
    with a:
        st.markdown(f'<div class="crumb">Home / Dashboard</div><div class="heading">Welcome back, {DASHBOARD_DATA["student"]["name"].split()[0]}</div><div class="subheading">Here\'s where your placement readiness stands today.</div>',unsafe_allow_html=True)
    with b:
        st.write(''); st.button('Update resume',use_container_width=True); st.button('Start mock interview',type='primary',use_container_width=True)
    st.write('')
    d=DASHBOARD_DATA['stats']; cols=st.columns(4)
    with cols[0]: metric('READINESS SCORE',f'{d["readiness"]}/100',f'<span style="color:#2dd4bf">{d["readiness_change"]}</span>')
    with cols[1]: metric('RESUME MATCH',f'{d["resume_match"]}%','against target roles','teal')
    with cols[2]: metric('SKILL GAPS OPEN',str(d['skill_gaps']),f'{d["high_priority"]} marked high priority','red')
    with cols[3]: metric('MOCK INTERVIEWS',str(d['mock_count']),f'<span style="color:#2dd4bf">{d["mock_average"]}</span> avg score /10','purple')
    st.write(''); left,right=st.columns([1.55,1])
    with left:
        st.markdown('<div class="panel"><div style="display:flex;justify-content:space-between"><div><div class="panel-title">Skill gap radar</div><div class="panel-sub">Your current strength vs. what target roles ask for</div></div><span style="color:#f5bd35;font-size:11px">View roadmap →</span></div>',unsafe_allow_html=True)
        for x in DASHBOARD_DATA['skills']:
            st.markdown(f'<div class="skill"><div class="skill-head"><b>{x["name"]}</b><span style="color:#8995a8">{x["score"]}%</span></div><div class="track"><div class="fill {x["color"]}" style="width:{x["score"]}%"></div></div></div>',unsafe_allow_html=True)
        st.markdown('</div><div class="panel"><div class="panel-title">Recommended for you</div><div class="panel-sub">Roles matched from your resume and skill profile</div>',unsafe_allow_html=True)
        for x in DASHBOARD_DATA['roles']:
            st.markdown(f'<div class="item"><div class="logo">{x["code"]}</div><div class="item-main"><div class="item-title">{x["role"]}</div><div class="item-detail">{x["details"]}</div></div><span class="badge {x["type"]}">{x["badge"]}</span></div>',unsafe_allow_html=True)
        st.markdown('</div>',unsafe_allow_html=True)
    with right:
        x=DASHBOARD_DATA['interview']
        st.markdown(f'<div class="panel"><div class="panel-title">Mock interview performance</div><div class="panel-sub">Last session: {x["last"]}</div><div class="interview"><div class="ring"><div class="ring-inner">{x["score"]}%</div></div><div class="feedback">{x["feedback"]}</div></div></div>',unsafe_allow_html=True)
        st.button('View feedback',use_container_width=True)
        st.markdown('<div class="panel"><div class="panel-title">Upcoming placement drives</div>',unsafe_allow_html=True)
        for x in DASHBOARD_DATA['drives']:
            st.markdown(f'<div class="item"><div class="logo">{x["code"]}</div><div class="item-main"><div class="item-title">{x["name"]}</div><div class="item-detail">{x["applied"]}</div></div><span class="badge {x["type"]}">{x["deadline"]}</span></div>',unsafe_allow_html=True)
        st.markdown('</div><div class="panel"><div class="panel-title">Quick actions</div><div class="quick"><div><span>▤</span>Resume scan</div><div><span>◎</span>Set target role</div><div><span>▦</span>Book mock</div></div></div>',unsafe_allow_html=True)

def assessment():
    st.markdown('<div class="crumb">Home / Student Assessment</div><div class="heading">Student Assessment</div><div class="subheading">Evaluate your technical readiness across core computer-science domains.</div><br>',unsafe_allow_html=True)
    c1,c2,c3=st.columns(3); name=c1.text_input('Student name',st.session_state.student)
    company=c2.selectbox('Target company',list(COMPANIES),index=list(COMPANIES).index(st.session_state.company)); roles=list(COMPANIES[company])
    role=c3.selectbox('Target role',roles,index=roles.index(st.session_state.role) if st.session_state.role in roles else 0)
    st.info(f'{len(QUESTIONS)} MCQs · {len(domains)} domains · 1 mark each · No negative marking')
    with st.form('assessment_form'):
        for domain in domains:
            st.markdown(f'### {domain}')
            for q in [q for q in QUESTIONS if q['domain']==domain]:
                st.markdown(f'**{q["id"]}. [{q["difficulty"]}] {q["question"]}**')
                opts=['— Select an answer —']+q['options']; old=st.session_state.answers.get(q['id'],'— Select an answer —')
                st.selectbox('Choose one',opts,index=opts.index(old) if old in opts else 0,key=f'ans_{q["id"]}',label_visibility='collapsed')
        submitted=st.form_submit_button('Submit assessment',type='primary',use_container_width=True)
    if submitted:
        st.session_state.answers={q['id']:st.session_state.get(f'ans_{q["id"]}','— Select an answer —') for q in QUESTIONS}
        st.session_state.submitted=True; st.session_state.student=name.strip() or 'Student'; st.session_state.company=company; st.session_state.role=role
        st.success('Assessment submitted. Open Skill Gap to view your results.')

def skill_gap():
    st.markdown('<div class="crumb">Home / Skill Gap</div><div class="heading">Skill Gap Analysis</div><div class="subheading">Compare assessment performance with the selected company-role profile.</div><br>',unsafe_allow_html=True)
    if not st.session_state.submitted:
        st.warning('Complete the Student Assessment first to generate your personal report.'); return
    score,pct,rows=report(st.session_state.answers); a,b,c=st.columns(3)
    a.metric('Readiness score',f'{pct:.1f}/100'); b.metric('Correct answers',f'{score}/{len(QUESTIONS)}'); c.metric('Domains assessed',len(domains))
    df=pd.DataFrame(rows); st.markdown('### Domain-wise performance'); st.bar_chart(df.set_index('Domain')['Score'],color='#2dd4bf'); st.dataframe(df,use_container_width=True,hide_index=True)
    req=COMPANIES[st.session_state.company][st.session_state.role]; gaps=[]
    for row in rows:
        target=req['domain_targets'].get(row['Domain'],60); gap=max(round(target-row['Score'],1),0)
        gaps.append({'Domain':row['Domain'],'Your score':row['Score'],'Illustrative role target':target,'Gap':gap,'Priority':'High' if gap>=20 else ('Improve' if gap else 'On track')})
    st.markdown(f'### {st.session_state.company} — {st.session_state.role}'); st.dataframe(pd.DataFrame(gaps),use_container_width=True,hide_index=True)
    st.caption('Company thresholds are illustrative project data, not official hiring criteria. Scoring is deterministic in this review prototype.')

def planned_page(title,description):
    st.markdown(f'<div class="crumb">Home / {title}</div><div class="heading">{title}</div><div class="subheading">{description}</div><br>',unsafe_allow_html=True)
    st.info(f'{title} is shown in the product navigation, but this module is planned for a later development milestone. It is not represented as a completed feature in this review build.')

if page=='Dashboard': dashboard()
elif page=='Student Assessment': assessment()
elif page=='Skill Gap': skill_gap()
elif page=='Resume Analyzer': planned_page('Resume Analyzer','Upload a resume and compare extracted skills with a target role.')
elif page=='Mock Interviews': planned_page('Mock Interviews','Practice technical and behavioral interviews and review feedback.')
elif page=='Learning Roadmap': planned_page('Learning Roadmap','Follow a personalized sequence of skills and preparation tasks.')
elif page=='Placement Drives': planned_page('Placement Drives','Explore relevant opportunities and track application deadlines.')
else: planned_page('Settings','Manage your student profile and preferences.')

st.markdown('<div style="text-align:center;color:#667286;font-size:10px;padding:24px 0">PrepPath · CareerPilot Placement Readiness Agent · Review prototype</div>',unsafe_allow_html=True)
