# Tomorrow's Project Progress Review — Speaking Notes

## 60-second project explanation
"CareerPilot is an AI-powered career and placement readiness system. It aims to assess a student's current technical skills, compare them with the requirements of a selected company and role, identify skill gaps, and recommend a personalized preparation path.

For this review, we have implemented an initial assessment prototype with 40 MCQs across eight core computer science domains. It automatically evaluates responses and generates domain-wise scores. We have also prepared structured company-role requirement profiles and a prototype comparison workflow that highlights areas needing improvement.

The current recommendation logic is rule-based and explainable. The next phase is to integrate the tools through an LLM-based agent, add coding assessments, persist student progress, and validate company requirements against current job descriptions."

## Demo sequence
1. Open the deployed Streamlit app.
2. Go to Student Assessment; show the 8 domains and 40 MCQs.
3. Answer questions and submit.
4. Open Results & Skill Gaps; show overall score and domain-wise chart.
5. Show comparison against selected company-role profile.
6. Open Company Requirements API; show structured JSON and download button.
7. Open Project Architecture; explain implemented vs planned components.

## Likely guide questions
**Q: Is this a real AI agent yet?**
A: "This review build demonstrates the core tools and workflow. The current scoring and recommendation rules are deterministic. The next phase is to connect these tools using an LLM-based orchestrator so the agent can select tools, interpret the student's goal and produce an adaptive plan. We are not claiming full agent autonomy in this build."

**Q: How did you decide company requirements?**
A: "The current profiles are illustrative prototypes based on recurring skill categories for entry-level software roles. We will validate and update them using specific public job descriptions, storing the source URL, date checked and required/preferred classification for every requirement."

**Q: How is the readiness score calculated?**
A: "The prototype calculates transparent overall and domain-wise MCQ percentages. It then compares domain scores with configurable role-profile thresholds. These thresholds are not official company cutoffs. A more robust readiness score will include coding performance, question difficulty and evidence from verified job descriptions."

**Q: Why use MCQs first?**
A: "MCQs let us validate the assessment flow and domain-level reporting quickly. Coding questions are planned next and will be evaluated with test cases in an isolated execution environment."

**Q: What is the API?**
A: "The company-role requirements are currently structured as JSON data exposed in the prototype UI. The next backend milestone is a REST endpoint that returns the same schema by company and role."

## Be transparent
Do not claim that live company APIs, LLM orchestration, coding execution, authentication, database persistence or adaptive tracking are already implemented. Present them as next milestones.
