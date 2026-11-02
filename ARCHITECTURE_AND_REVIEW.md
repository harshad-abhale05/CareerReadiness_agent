# CareerPilot — Architecture and Review Notes

## Architecture (current MVP)
```text
Student
  |
  v
Streamlit Web Interface
  |-----------------------------|
  v                             v
Assessment UI               Company/Role Selector
  |                             |
  v                             v
Question Bank (JSON)         Requirements Profiles (JSON)
  |                             |
  v                             |
Deterministic Evaluation Engine |
  |                             |
  +-------------+---------------+
                |
                v
        Skill Gap Analyzer
                |
                v
     Rule-based Recommendations
                |
                v
      Domain-wise Readiness Report
```

## Target architecture
```text
React Web Client
      |
Node.js REST API ---- PostgreSQL/Supabase
      |                       |
      +---- Assessment Service|
      +---- Company Data API--+
      |
Python Agent Service (LangGraph)
      |
      +-- get_assessment_result()
      +-- get_company_requirements()
      +-- analyze_skill_gaps()
      +-- create_study_plan()
      +-- track_progress()
      |
LLM reasoning + deterministic scoring tools
```

## Scoring methodology
- Each MCQ is worth 1 mark.
- No negative marking in the prototype.
- Overall percentage = correct answers / total questions × 100.
- Domain percentage = correct answers in domain / questions in domain × 100.
- The role profile stores illustrative domain thresholds; gap = max(threshold - student score, 0).
- Thresholds are prototype assumptions, not official employer cutoffs.

## Review status
Implemented: 40-question MCQ bank, browser-based assessment, scoring, domain breakdown, company-role profile viewer, gap comparison, rule-generated recommendations.

Planned: coding execution in a sandbox, database persistence, authenticated users, job-posting ingestion, source verification, LLM agent orchestration, adaptive study plans, progress tracking, automated tests.
