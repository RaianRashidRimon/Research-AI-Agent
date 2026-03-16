import streamlit as st
from dotenv import load_dotenv
from graph import run_pipeline

load_dotenv()

st.set_page_config(
    page_title="Multi-Agent Research Assistant",
    page_icon="🔬",
    layout="wide"
)

# Sidebar
with st.sidebar:
    st.title("🔬 Research Assistant")
    st.markdown("A multi-agent AI research tool powered by Gemini.")
    st.divider()

    if "last_result" in st.session_state:
        result = st.session_state.last_result
        st.subheader("Last Run Info")

        confidence_map = {
            "high":   ("✅ HIGH",   "green"),
            "medium": ("⚠️ MEDIUM", "orange"),
            "low":    ("❌ LOW",    "red"),
        }
        label, color = confidence_map.get(result.confidence, ("❓ UNKNOWN", "gray"))
        st.markdown(f"**Confidence:** :{color}[{label}]")

        if result.flagged_claims:
            st.subheader("⚠️ Flagged Claims")
            for claim in result.flagged_claims:
                st.warning(claim)
        else:
            st.success("No claims flagged.")

        if result.sources:
            st.subheader("📚 Sources")
            for source in result.sources:
                if source and source.strip():
                    st.markdown(f"- {source}")

        st.divider()
        if st.button("💾 Save Last Report"):
            from tools import save_to_txt
            content = f"Topic: {result.topic}\n\nSummary:\n{result.verified_summary}\n\nKey Points:\n"
            content += "\n".join(f"- {p}" for p in result.key_points)
            if result.flagged_claims:
                content += "\n\nFlagged Claims:\n"
                content += "\n".join(f"- {c}" for c in result.flagged_claims)
            content += f"\n\nConfidence: {result.confidence.upper()}"
            content += f"\n\nSources:\n" + "\n".join(result.sources)
            save_to_txt(content)
            st.success("Report saved to research_output.txt")

    st.divider()
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.session_state.pop("last_result", None)
        st.rerun()

# Chat history init
if "messages" not in st.session_state:
    st.session_state.messages = []

# Title
st.title("🔬 Multi-Agent Research Assistant")
st.caption("Powered by Researcher → Writer → Fact Checker pipeline")

# Render past messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("What do you want to research?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Running research pipeline..."):
            col1, col2, col3 = st.columns(3)
            with col1:
                st.info("🔍 Researcher gathering facts...")
            with col2:
                st.info("✍️ Writer structuring summary...")
            with col3:
                st.info("✅ Fact Checker verifying claims...")

            result = run_pipeline(prompt)
            st.session_state.last_result = result

        confidence_map = {
            "high":   ("✅ HIGH",   "green"),
            "medium": ("⚠️ MEDIUM", "orange"),
            "low":    ("❌ LOW",    "red"),
        }
        label, color = confidence_map.get(result.confidence, ("❓ UNKNOWN", "gray"))

        response_md = f"""
### {result.topic}

{result.verified_summary}

---

**Key Points:**
{chr(10).join(f"- {p}" for p in result.key_points)}

**Confidence:** :{color}[{label}]
"""
        if result.flagged_claims:
            response_md += f"\n\n**⚠️ Flagged Claims:**\n"
            response_md += "\n".join(f"- {c}" for c in result.flagged_claims)

        st.markdown(response_md)
        st.session_state.messages.append({"role": "assistant", "content": response_md})