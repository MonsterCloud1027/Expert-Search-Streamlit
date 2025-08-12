import streamlit as st

st.set_page_config(page_title="User Study")
st.title("User Study")

st.markdown(
    """
    Please participate in our user study by clicking the link below:
    [👉 Click here to start the User Study](https://your-userstudy-link.com)
    """,
    unsafe_allow_html=True
)
st.markdown("## User Study Overview")

st.markdown("""
### 🎯 Research Objectives
- Compare the impact of three expert recommendation presentation modes on user decision-making and experience:
  1. **Visualization Only**: Display expert network, research topics, and other visual analytics only.
  2. **LLM Explanation Only**: Display only LLM-generated textual recommendation reasons.
  3. **Combined**: Display both visualization and LLM-generated explanations together.
- Theoretical foundations:
  - **Dual Coding Theory**: Combined presentation may improve understanding and decision confidence.
  - **Cognitive Load Theory**: Different presentation modes may lead to different cognitive load profiles.

### 📋 Key Measures
1. **Reasoning Quality**
   - After selecting an expert, participants provide a short written reason.
   - Independent evaluators score reasons based on a rubric:
     - Relevance to the task/topic
     - Evidence from visualization
     - Evidence from textual explanation
     - Logical coherence of reasoning
2. **Confidence & Understanding**
   - 1–7 Likert scale ratings after each selection.
3. **Cognitive Load & Completion Time**
   - NASA-TLX (or simplified version) after each condition.
   - completion time per task.

### 🧪 Experimental Design
- **Design type**: Within-subject (each participant experiences all three conditions).
- **Task**:
  - Given a research topic, select the most suitable expert from a Top 5 list.
- **Per-task procedure**:
  1. Read task instructions
  2. View Top 5 experts (in the current presentation mode)
  3. Select an expert
  4. Provide reasoning
  5. Rate confidence (1–7)
  6. Rate understanding (1–7)
  7. Completion time is recorded automatically
- **After each condition**: Complete NASA-TLX questionnaire

### 📊 Data Analysis
- Repeated measures ANOVA / Friedman Test to compare conditions on:
  - Reasoning quality
  - Confidence & understanding
  - Completion time & cognitive load
- Report effect sizes (η² / r)
""")