```python
import json
from html import escape
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

NAV_ITEMS = ['Dashboard', 'Resume Analyzer', 'Student Assessment', 'Skill Gap',
             'Mock Interviews', 'Learning Roadmap', 'Placement Drives', 'Settings']
UNANSWERED = '— Select an answer —'

# Static profile shown in the sidebar. This is not assessment data.
PROFILE = {'name': 'Harshad Abhale', 'degree': 'B.Tech CSE · Final Year'}

# SAMPLE / DEMO DATA ONLY. Kept separate from student results and always labelled in the UI.
# Nothing in this block is derived from the student's activity or from live listings.
DEMO_ROLES = [
    {'code': 'TCS', 'role': 'Software Engineer — TCS Digital', 'details': 'Sample listing · not a live or verified opportunity'},
    {'code': 'INF', 'role': 'Backend Developer — Infosys', 'details': 'Sample listing · not a live or verified opportunity'},
    {'code': 'AMZ', 'role': 'SDE Intern — Amazon', 'details': 'Sample listing · not a live or verified opportunity'},
]
DEMO_DRIVES = [
    {'code': 'GO', 'name': 'Google — SWE Intern', 'details': 'Sample drive · dates not real'},
    {'code': 'MS', 'name': 'Microsoft — Data Analyst', 'details': 'Sample drive · dates not real'},
]

st.set_page_config(page_title='PrepPath | Placement Readiness', page_icon='🎓', layout='wide', initial_sidebar_state='auto')  # 'auto' = open on desktop, collapsed on phones

st.markdown(r'''<style>
:root{--bg:#0b0e14;--side:#10141d;--card:#121720;--border:#252d3a;--text:#edf1f8;--muted:#8995a8;--gold:#f5bd35;--teal:#2dd4bf;--red:#fa7567;--purple:#9b8cff}
.stApp{background:var(--bg);color:var(--text)} [data-testid="stHeader"]{background:rgba(11,14,20,.96)}
.block-container{max-width:1500px;padding-top:3.6rem;padding-bottom:2rem}
section[data-testid="stSidebar"]{background:var(--side);border-right:1px solid var(--border)}
section[data-testid="stSidebar"]>div{padding-top:1.2rem} section[data-testid="stSidebar"] *{color:var(--text)}
.brand{display:flex;align-items:center;gap:11px;padding:8px 5px 27px}
.brand-icon{width:39px;height:39px;border-radius:10px;background:var(--gold);color:#15120a!important;display:flex;align-items:center;justify-content:center;font-weight:900}
.brand-name{font-size:17px;font-weight:800}.brand-sub{font-size:11px;color:var(--muted)!important;margin-top:3px}
.userbox{display:flex;align-items:center;gap:10px;border:1px solid var(--border);background:#171d29;border-radius:11px;padding:11px;margin-top:22px}
.avatar{width:35px;height:35px;border-radius:50%;background:#7564d9;display:flex;align-items:center;justify-content:center;font-weight:800}
.user-name{font-size:12px;font-weight:700}.user-degree{font-size:10px;color:var(--muted)!important;margin-top:3px}
.crumb{font-size:12px;color:var(--muted);margin-bottom:7px}.heading{font-size:27px;font-weight:800;color:#f1f4fa}.subheading{font-size:13px;color:var(--muted);margin-top:5px}
.metric{background:var(--card);border:1px solid var(--border);border-left:3px solid var(--gold);border-radius:12px;padding:15px 16px;min-height:132px}
.metric.teal{border-left-color:var(--teal)}.metric.red{border-left-color:var(--red)}.metric.purple{border-left-color:var(--purple)}
.metric-label{font-size:10px;letter-spacing:.7px;color:var(--muted)}.metric-value{font-size:27px;font-weight:800;margin-top:8px}.metric-value.small{font-size:19px;line-height:1.6;color:#b4bfce}.metric-help{font-size:11px;color:var(--muted);margin-top:4px}
.panel{background:var(--card);border:1px solid var(--border);border-radius:13px;padding:18px;margin-bottom:15px}
.panel-title{font-size:15px;font-weight:750;color:#f1f4f9}.panel-sub{font-size:11px;color:var(--muted);margin-top:4px}
.skill{margin-top:17px}.skill-head{display:flex;justify-content:space-between;font-size:12px;margin-bottom:7px}.track{height:6px;background:#252d3a;border-radius:20px;overflow:hidden}.fill{height:100%;border-radius:20px}.fill.teal{background:var(--teal)}.fill.gold{background:var(--gold)}.fill.red{background:var(--red)}
.item{display:flex;align-items:center;gap:11px;padding:13px 0;border-bottom:1px solid var(--border)}.item:last-child{border:0;padding-bottom:0}
.logo{width:35px;height:35px;flex-shrink:0;border-radius:9px;background:#1c2432;color:var(--gold);display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:800}
.item-main{flex:1;min-width:0}.item-title{font-size:12px;font-weight:700}.item-detail{font-size:10px;color:var(--muted);margin-top:4px}
.badge{padding:5px 9px;border-radius:20px;font-size:10px;font-weight:700;white-space:nowrap}.badge.good{color:var(--teal);background:#12312f}.badge.warning{color:var(--red);background:#382321}.badge.demo{color:var(--purple);background:#262046}
.ring{width:78px;height:78px;border-radius:50%;background:conic-gradient(var(--teal) 0 76%,#27313d 76% 100%);display:flex;align-items:center;justify-content:center;flex-shrink:0}.ring.empty{background:#27313d}.ring-inner{width:62px;height:62px;border-radius:50%;background:var(--card);display:flex;align-items:center;justify-content:center;font-size:17px;font-weight:800}
.interview{display:flex;align-items:center;gap:15px;margin:17px 0 14px}.feedback{font-size:11px;line-height:1.55;color:#b4bfce}
.status{display:flex;flex-wrap:wrap;gap:8px 18px;align-items:center;font-size:12px;color:var(--muted);margin:2px 0 4px}.status b{color:var(--text)}
.dot{display:inline-block;width:8px;height:8px;border-radius:50%;margin-right:6px;background:var(--red)}.dot.ok{background:var(--teal)}
.sample-tag{display:inline-block;font-size:10px;font-weight:700;color:var(--purple);background:#262046;border-radius:20px;padding:3px 9px;margin-left:8px;vertical-align:middle}
div.stButton>button{background:#171e29;color:#e9eef7;border:1px solid #303949;border-radius:8px;font-size:12px;transition:.2s}
div.stButton>button:hover{border-color:var(--gold);color:var(--gold);background:#202938}
div.stButton>button[kind="primary"]{background:var(--gold);color:#15120a;border:1px solid var(--gold);font-weight:800}
div.stButton>button[kind="primary"]:hover{background:#ffd15c;color:#15120a}
[data-testid="stMetric"]{background:var(--card);border:1px solid var(--border);border-radius:11px;padding:12px}
.stTextInput input,.stSelectbox div[data-baseweb="select"]>div{background:#151b25;color:var(--text);border-color:#303949}
/* ---- Responsive layout ---- */
.stApp,[data-testid="stAppViewContainer"],[data-testid="stMain"]{overflow-x:hidden}
img,table,pre,iframe{max-width:100%}
.item-title,.item-detail,.feedback,.panel-sub{overflow-wrap:anywhere}
[data-testid="stDataFrame"]{max-width:100%}
@media(max-width:992px){
  .block-container{padding-left:1.2rem;padding-right:1.2rem}
  [data-testid="stHorizontalBlock"]{flex-wrap:wrap!important;gap:.75rem!important}
  [data-testid="stHorizontalBlock"]>[data-testid="stColumn"],[data-testid="stHorizontalBlock"]>[data-testid="column"]{flex:1 1 calc(50% - .75rem)!important;min-width:calc(50% - .75rem)!important;width:auto!important}
  [data-testid="stHorizontalBlock"]:has(.panel)>[data-testid="stColumn"],[data-testid="stHorizontalBlock"]:has(.panel)>[data-testid="column"],
  [data-testid="stHorizontalBlock"]:has(.heading)>[data-testid="stColumn"],[data-testid="stHorizontalBlock"]:has(.heading)>[data-testid="column"]{flex:1 1 100%!important;min-width:100%!important}
}
@media(max-width:640px){
  .block-container{padding:4.2rem .75rem 2rem}
  .metric{margin-bottom:.6rem}
  [data-testid="stHorizontalBlock"]>[data-testid="stColumn"],[data-testid="stHorizontalBlock"]>[data-testid="column"]{flex:1 1 100%!important;min-width:100%!important}
  .heading{font-size:21px}.metric{min-height:0}.metric-value{font-size:23px}.panel{padding:14px}
  .interview{flex-direction:column;align-items:flex-start}
  div.stButton>button{width:100%}
}
</style>''', unsafe_allow_html=True)

# ---------------------------------------------------------------- session state
ss = st.session_state
ss.setdefault('student', PROFILE['name'])
ss.setdefault('company', list(COMPANIES)[0])
ss.setdefault('role', list(COMPANIES[ss.company])[0])
ss.setdefault('attempt', 0)        # bumped on every retake so old widget values are never reused
ss.setdefault('results', None)     # None until the student submits the assessment
ss.setdefault('nav', 'Dashboard')
domains = list(dict.fromkeys(q['domain'] for q in QUESTIONS))


def go(page_name):
    """Callback used by buttons to switch the sidebar page."""
    st.session_state.nav = page_name


def retake():
    st.session_state.attempt += 1
    st.session_state.results = None
    st.session_state.nav = 'Student Assessment'


def initials(name):
    parts = [p for p in name.split() if p]
    return escape(''.join(p[0] for p in parts[:2]).upper() or 'ST')


with st.sidebar:
    st.markdown('<div class="brand"><div class="brand-icon">PP</div><div><div class="brand-name">PrepPath</div><div class="brand-sub">Placement Readiness</div></div></div>', unsafe_allow_html=True)
    st.caption('WORKSPACE')
    page = st.radio('Navigation', NAV_ITEMS, key='nav', label_visibility='collapsed')
    st.markdown(f'<div class="userbox"><div class="avatar">{initials(ss.student)}</div><div><div class="user-name">{escape(ss.student)}</div><div class="user-degree">{PROFILE["degree"]}</div></div></div>', unsafe_allow_html=True)
    st.caption('⚙ Settings')


# ---------------------------------------------------------------- scoring (unchanged logic)
def report(answers):
    total=len(QUESTIONS); score=sum(1 for q in QUESTIONS if answers.get(q['id'])==q['correct_answer'])
    rows=[]
    for domain in domains:
        qs=[q for q in QUESTIONS if q['domain']==domain]
        correct=sum(1 for q in qs if answers.get(q['id'])==q['correct_answer'])
        rows.append({'Domain':domain,'Score':round(correct/len(qs)*100,1),'Correct':f'{correct}/{len(qs)}'})
    return score, score/total*100 if total else 0, rows


def compute_gaps(rows, company, role):
    """Compare domain scores with the illustrative targets of the chosen company-role."""
    req = COMPANIES[company][role]; gaps = []
    for row in rows:
        target = req['domain_targets'].get(row['Domain'], 60); gap = max(round(target - row['Score'], 1), 0)
        gaps.append({'Domain': row['Domain'], 'Your score': row['Score'], 'Illustrative role target': target, 'Gap': gap,
                     'Priority': 'High' if gap >= 20 else ('Improve' if gap else 'On track')})
    return gaps


def build_results(answers, student, company, role):
    score, pct, rows = report(answers)
    return {'score': score, 'pct': pct, 'rows': rows, 'gaps': compute_gaps(rows, company, role),
            'company': company, 'role': role, 'student': student, 'total': len(QUESTIONS),
            'unanswered': sum(1 for q in QUESTIONS if answers.get(q['id'], UNANSWERED) == UNANSWERED)}


# ---------------------------------------------------------------- UI helpers
def metric(label,value,help_text,accent='',small=False):
    cls = 'metric-value small' if small else 'metric-value'
    st.markdown(f'<div class="metric {accent}"><div class="metric-label">{label}</div><div class="{cls}">{value}</div><div class="metric-help">{help_text}</div></div>',unsafe_allow_html=True)


def bar_color(gap):
    return 'teal' if gap == 0 else ('gold' if gap < 20 else 'red')


def dashboard():
    r = ss.results
    a,b=st.columns([3,1.15])
    with a:
        st.markdown(f'<div class="crumb">Home / Dashboard</div><div class="heading">Welcome back, {escape(ss.student.split()[0])}</div><div class="subheading">Here\'s where your placement readiness stands today.</div>',unsafe_allow_html=True)
    with b:
        st.write(''); st.button('Update Resume',use_container_width=True,on_click=go,args=('Resume Analyzer',)); st.button('Start Mock Interview',type='primary',use_container_width=True,on_click=go,args=('Mock Interviews',))
    st.write(''); cols=st.columns(4)
    with cols[0]:
        if r: metric('READINESS SCORE',f'{r["pct"]:.1f}/100',f'{r["score"]}/{r["total"]} correct · from your assessment')
        else: metric('READINESS SCORE','Not assessed','Complete the Student Assessment',small=True)
    with cols[1]: metric('RESUME MATCH','—','Resume Analyzer is a planned module','teal')
    with cols[2]:
        if r:
            high=sum(1 for g in r['gaps'] if g['Priority']=='High'); open_gaps=sum(1 for g in r['gaps'] if g['Gap']>0)
            metric('SKILL GAPS OPEN',str(open_gaps),f'{high} marked high priority','red')
        else: metric('SKILL GAPS OPEN','Not available','Appears after the assessment','red',small=True)
    with cols[3]: metric('MOCK INTERVIEWS','—','Planned module · no sessions recorded','purple')
    if r: status=f'<span><span class="dot ok"></span><b>Assessment status:</b> Completed</span><span><b>Target:</b> {escape(r["company"])} — {escape(r["role"])}</span>'
    else: status='<span><span class="dot"></span><b>Assessment status:</b> Not completed</span>'
    st.markdown(f'<div class="status">{status}</div>',unsafe_allow_html=True)
    st.write(''); left,right=st.columns([1.55,1])
    with left:
        if r:
            sub=f'Your assessment scores vs. illustrative targets for {escape(r["company"])} — {escape(r["role"])}'
            bars=''.join(f'<div class="skill"><div class="skill-head"><b>{escape(g["Domain"])}</b><span style="color:#8995a8">{g["Your score"]:g}% · target {g["Illustrative role target"]}%</span></div><div class="track"><div class="fill {bar_color(g["Gap"])}" style="width:{min(g["Your score"],100)}%"></div></div></div>' for g in r['gaps'])
        else:
            sub='Skill performance: Not assessed'
            bars='<div class="skill"><div class="metric-help">No skill data yet. Open <b>Student Assessment</b> and submit the exam to see your domain-wise performance here.</div></div>'
        st.markdown(f'<div class="panel"><div class="panel-title">Skill Gap Analysis</div><div class="panel-sub">{sub}</div>{bars}</div>',unsafe_allow_html=True)
        roles=''.join(f'<div class="item"><div class="logo">{x["code"]}</div><div class="item-main"><div class="item-title">{x["role"]}</div><div class="item-detail">{x["details"]}</div></div><span class="badge demo">Sample</span></div>' for x in DEMO_ROLES)
        st.markdown(f'<div class="panel"><div class="panel-title">Recommended Roles<span class="sample-tag">SAMPLE DATA</span></div><div class="panel-sub">Illustrative examples only. Role matching is not implemented yet.</div>{roles}</div>',unsafe_allow_html=True)
    with right:
        st.markdown('<div class="panel"><div class="panel-title">Mock Interview Performance</div><div class="panel-sub">Planned feature</div><div class="interview"><div class="ring empty"><div class="ring-inner">—</div></div><div class="feedback">Not available yet. Mock interviews are planned for a later milestone, so no scores are shown.</div></div></div>',unsafe_allow_html=True)
        drives=''.join(f'<div class="item"><div class="logo">{x["code"]}</div><div class="item-main"><div class="item-title">{x["name"]}</div><div class="item-detail">{x["details"]}</div></div><span class="badge demo">Sample</span></div>' for x in DEMO_DRIVES)
        st.markdown(f'<div class="panel"><div class="panel-title">Upcoming Placement Drives<span class="sample-tag">SAMPLE DATA</span></div><div class="panel-sub">Not live listings.</div>{drives}</div>',unsafe_allow_html=True)
        st.markdown('<div class="panel" style="margin-bottom:8px"><div class="panel-title">Quick Actions</div></div>',unsafe_allow_html=True)
        st.button('📝 Take student assessment',type='primary',use_container_width=True,on_click=go,args=('Student Assessment',))
        st.button('📊 View skill gap',use_container_width=True,on_click=go,args=('Skill Gap',))
        st.button('📄 Resume scan (planned)',use_container_width=True,on_click=go,args=('Resume Analyzer',))


def assessment():
    st.markdown('<div class="crumb">Home / Student Assessment</div><div class="heading">Student Assessment</div><div class="subheading">Evaluate your technical readiness across core computer-science domains.</div><br>',unsafe_allow_html=True)
    r = ss.results
    if r:
        st.success('Assessment submitted. Your results are below and the dashboard has been updated.')
        a,b,c=st.columns(3)
        a.metric('Readiness score',f'{r["pct"]:.1f}/100'); b.metric('Correct answers',f'{r["score"]}/{r["total"]}'); c.metric('Target',f'{r["company"]}')
        if r['unanswered']: st.caption(f'{r["unanswered"]} question(s) were left unanswered and counted as incorrect.')
        st.dataframe(pd.DataFrame(r['rows']),use_container_width=True,hide_index=True)
        x,y,z=st.columns(3)
        x.button('View skill gap analysis',type='primary',use_container_width=True,on_click=go,args=('Skill Gap',))
        y.button('Open dashboard',use_container_width=True,on_click=go,args=('Dashboard',))
        z.button('Retake assessment',use_container_width=True,on_click=retake)
        return
    attempt = ss.attempt
    c1,c2,c3=st.columns(3); name=c1.text_input('Student name',ss.student,key=f'name_{attempt}')
    company=c2.selectbox('Target company',list(COMPANIES),index=list(COMPANIES).index(ss.company),key=f'company_{attempt}'); roles=list(COMPANIES[company])
    role=c3.selectbox('Target role',roles,index=roles.index(ss.role) if ss.role in roles else 0,key=f'role_{attempt}_{company}')
    st.info(f'{len(QUESTIONS)} MCQs · {len(domains)} domains · 1 mark each · No negative marking')
    with st.form(f'assessment_form_{attempt}'):
        for domain in domains:
            st.markdown(f'### {domain}')
            for q in [q for q in QUESTIONS if q['domain']==domain]:
                st.markdown(f'**{q["id"]}. [{q["difficulty"]}] {q["question"]}**')
                st.selectbox('Choose one',[UNANSWERED]+q['options'],key=f'ans_{attempt}_{q["id"]}',label_visibility='collapsed')
        submitted=st.form_submit_button('Submit assessment',type='primary',use_container_width=True)
    if submitted:
        answers={q['id']:st.session_state.get(f'ans_{attempt}_{q["id"]}',UNANSWERED) for q in QUESTIONS}
        ss.student=name.strip() or 'Student'; ss.company=company; ss.role=role
        ss.results=build_results(answers,ss.student,company,role)
        st.rerun()


def skill_gap():
    st.markdown('<div class="crumb">Home / Skill Gap</div><div class="heading">Skill Gap Analysis</div><div class="subheading">Compare assessment performance with the selected company-role profile.</div><br>',unsafe_allow_html=True)
    r = ss.results
    if not r:
        st.warning('Complete the Student Assessment first to generate your personal report.')
        st.button('Go to Student Assessment',type='primary',on_click=go,args=('Student Assessment',)); return
    a,b,c=st.columns(3)
    a.metric('Readiness score',f'{r["pct"]:.1f}/100'); b.metric('Correct answers',f'{r["score"]}/{r["total"]}'); c.metric('Domains assessed',len(domains))
    df=pd.DataFrame(r['rows']); st.markdown('### Domain-wise performance'); st.bar_chart(df.set_index('Domain')['Score'],color='#2dd4bf'); st.dataframe(df,use_container_width=True,hide_index=True)
    st.markdown(f'### {r["company"]} — {r["role"]}'); st.dataframe(pd.DataFrame(r['gaps']),use_container_width=True,hide_index=True)
    st.caption('Company thresholds are illustrative project data, not official hiring criteria. Scoring is deterministic in this review prototype.')
    st.button('Retake assessment',on_click=retake)


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