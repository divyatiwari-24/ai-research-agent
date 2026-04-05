import streamlit as st
from agents import multi_agent_system
import time
import json

st.set_page_config(page_title="AI Research Assistant", layout="wide")

# ---- Session State for Chat History ----
if "history" not in st.session_state:
    st.session_state.history = []

# ---- Minimal Clean Styling ----
st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
}
</style>
""", unsafe_allow_html=True)

# ---- Header ----
st.title("Autonomous AI Research Assistant")
st.caption("Multi-Agent System: Planner • Researcher • Writer")

# ---- Input ----
query = st.text_input("Enter your question")

# ---- Buttons Row ----
col_btn1, col_btn2 = st.columns([1, 1])

with col_btn1:
    run_clicked = st.button("Run Research")

with col_btn2:
    if st.button("Clear History"):
        st.session_state.history = []

# ---- Display Chat History ----
if st.session_state.history:
    st.markdown("## Previous Conversations")

    for chat in reversed(st.session_state.history):
        with st.expander(f"Question: {chat['query']}"):
            st.markdown("**Planner**")
            st.write(chat["plan"])

            st.markdown("**Research**")
            st.write(chat["research"])

            st.markdown("**Final Answer**")
            st.write(chat["answer"])

# ---- Run Logic ----
if run_clicked:
    if query:
        with st.spinner("Processing..."):
            time.sleep(1)
            result = multi_agent_system(query)

        # ---- Clean JSON Output ----
        result = result.strip()

        if result.startswith("```"):
            result = result.replace("```json", "").replace("```", "").strip()

        if "{" in result:
            result = result[result.find("{"):result.rfind("}")+1]

        # Default values
        plan, research, answer = "", "", ""

        try:
            data = json.loads(result)

            plan = str(data.get("plan", "No plan generated"))
            research = str(data.get("research", "No research generated"))
            answer = str(data.get("answer", "No answer generated"))

        except Exception as e:
            st.error(f"Parsing failed: {e}")
            st.text(result)

        # ---- Save to history ----
        st.session_state.history.append({
            "query": query,
            "plan": plan,
            "research": research,
            "answer": answer
        })

        # Optional: limit history to last 5
        if len(st.session_state.history) > 5:
            st.session_state.history.pop(0)

        # ---- Output Layout ----
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Planner Output")
            st.text_area("", plan, height=250)
            st.button("Copy Plan", on_click=lambda: st.session_state.update({"copy": plan}))

        with col2:
            st.subheader("Research Output")
            st.text_area("", research, height=250)
            st.button("Copy Research", on_click=lambda: st.session_state.update({"copy": research}))

        st.divider()

        st.subheader("Final Answer")
        st.success(answer)
        st.button("Copy Answer", on_click=lambda: st.session_state.update({"copy": answer}))