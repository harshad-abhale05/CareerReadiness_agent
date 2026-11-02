# CareerPilot Review MVP

A deployable Streamlit prototype for a final-year project progress review.

## Included
- 40 MCQs across 8 core CS domains (5 per domain).
- Three difficulty labels: Beginner, Intermediate, Advanced.
- Automatic scoring and domain-wise performance.
- Company/role requirements JSON profiles for Google, Microsoft, Amazon, TCS and Infosys.
- Rule-based skill-gap comparison and recommendations.
- Architecture view and implementation status.

## Deploy online (no localhost required)
1. Create a GitHub repository, e.g. `careerpilot-review-mvp`.
2. Upload all files and folders from this project.
3. Open https://share.streamlit.io/ and sign in with GitHub.
4. Choose the repository, branch, and `app.py`.
5. Click Deploy. The app will receive a public Streamlit URL.

## Important scope notes
- Company profiles are illustrative prototype profiles, not official company APIs or universal hiring criteria. Validate against specific current job descriptions before making claims.
- Current recommendation logic is deterministic/rule-based. LLM + LangGraph tool orchestration is a planned next phase.
- Coding assessment, authentication, persistent database, adaptive study plans and progress history are not yet implemented.
- This MVP is for demonstrating project progress, not a validated hiring or psychometric assessment.
