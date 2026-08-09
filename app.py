import streamlit as st

st.set_page_config(
    page_title="GovSchemeAI",
    page_icon="🌾",
    layout="wide"
)

st.title("🌾 GovSchemeAI")
st.subheader("Government Scheme Assistant")

st.success("GovSchemeAI is running successfully!")

st.write(
    "Find government schemes, ask questions using AI, "
    "and check your eligibility."
)

st.divider()

st.header("What do you want to do?")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("🤖 AI Chat")
    st.write(
        "Ask questions about government schemes "
        "in simple language."
    )

    if st.button("Open AI Chat", use_container_width=True):
        st.switch_page("pages/1_AI_Chat.py")


with col2:
    st.subheader("🔎 Find Schemes")
    st.write(
        "Search government schemes by state, "
        "district, category and crop."
    )

    if st.button("Find Schemes", use_container_width=True):
        st.switch_page("pages/2_Find_Schemes.py")


with col3:
    st.subheader("🎯 Eligibility")
    st.write(
        "Check whether you may be eligible "
        "for available government schemes."
    )

    if st.button("Check Eligibility", use_container_width=True):
        st.switch_page("pages/3_Eligibility.py")


st.divider()

st.header("Platform")

a, b, c = st.columns(3)

with a:
    st.metric("Government Schemes", "500+")

with b:
    st.metric("RAG Database", "500")

with c:
    st.metric("AI Assistant", "Online")


st.divider()

st.caption(
    "🌾 GovSchemeAI — Making government schemes easier "
    "to discover and understand."
)