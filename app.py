import streamlit as st
from agents import run_pipeline_streaming

st.set_page_config(
    page_title="Research Pipeline",
    layout="centered",
)

st.title("AI Research Pipeline")
st.caption("Multi agent user reserach pipeline that generates user insights and a polished research report from a realistic user interview.")

st.divider()

topic = st.text_input(
    "Research Topic",
    placeholder="e.g. remote work tools, fitness apps, online learning platforms",

)

if st.button("Run Pipeline", type="primary", disabled=not topic):
    st.divider()
    
    # Agent 1
    with st.status("Agent 1 — Moderator is conducting the interview...", expanded=True) as status1:
        st.write("Generating a realistic user interview transcript...")
        transcript = run_pipeline_streaming("interview", topic)
        status1.update(label="Agent 1 — Interview complete", state="complete", expanded=False)

    # Agent 2
    with st.status("Agent 2 — Analyst is extracting insights...", expanded=True) as status2:
        st.write("Identifying themes, pain points, and key quotes...")
        insights = run_pipeline_streaming("analysis", topic, transcript)
        status2.update(label="Agent 2 — Insights extracted", state="complete", expanded=False)

    # Agent 3
    with st.status("Agent 3 — Reporter is writing the report...", expanded=True) as status3:
        st.write("Compiling a shareable research summary...")
        report = run_pipeline_streaming("report", topic, insights)
        status3.update(label="Agent 3 — Report ready", state="complete", expanded=False)

    st.success("Pipeline complete.")
    st.divider()

    with st.expander("Interview Transcript", expanded=False):
        st.markdown(transcript)

    with st.expander("Extracted Insights", expanded=False):
        st.markdown(insights)

    with st.expander("Research Report", expanded=True):
        st.markdown(report)