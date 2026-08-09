import streamlit as st

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="GovSchemeAI",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* Main background */
    .stApp {
        background: #f7faf8;
    }

    /* Main content width */
    .block-container {
        max-width: 1200px;
        padding-top: 3rem;
        padding-bottom: 3rem;
    }

    /* Hide Streamlit default menu */
    #MainMenu {
        visibility: hidden;
    }

    /* Header */
    .hero {
        background: linear-gradient(
            135deg,
            #166534 0%,
            #15803d 100%
        );

        padding: 55px 60px;
        border-radius: 28px;
        margin-bottom: 35px;
        color: white;
        box-shadow: 0 15px 40px rgba(22, 101, 52, 0.18);
    }

    .hero-badge {
        display: inline-block;
        background: rgba(255,255,255,0.15);
        border: 1px solid rgba(255,255,255,0.25);
        padding: 8px 16px;
        border-radius: 30px;
        font-size: 14px;
        margin-bottom: 20px;
    }

    .hero h1 {
        font-size: 48px;
        line-height: 1.1;
        margin: 0;
        font-weight: 800;
    }

    .hero h1 span {
        color: #facc15;
    }

    .hero p {
        font-size: 19px;
        line-height: 1.6;
        max-width: 700px;
        margin-top: 20px;
        color: #e8f5e9;
    }

    /* Section headings */
    .section-title {
        font-size: 30px;
        font-weight: 800;
        color: #172018;
        margin-top: 35px;
        margin-bottom: 5px;
    }

    .section-subtitle {
        color: #64748b;
        font-size: 16px;
        margin-bottom: 25px;
    }

    /* Cards */
    .feature-card {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 20px;
        padding: 28px;
        min-height: 220px;
        box-shadow: 0 8px 25px rgba(15, 23, 42, 0.06);
    }

    .feature-icon {
        font-size: 38px;
        margin-bottom: 15px;
    }

    .feature-card h3 {
        color: #172018;
        font-size: 22px;
        margin-bottom: 10px;
    }

    .feature-card p {
        color: #64748b;
        line-height: 1.6;
    }

    /* Statistics */
    .stat-card {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 18px;
        padding: 25px;
        text-align: center;
        box-shadow: 0 6px 20px rgba(15, 23, 42, 0.05);
    }

    .stat-number {
        font-size: 34px;
        font-weight: 800;
        color: #166534;
    }

    .stat-label {
        color: #64748b;
        margin-top: 5px;
    }

    /* Footer */
    .footer {
        margin-top: 60px;
        padding: 30px;
        text-align: center;
        border-top: 1px solid #e2e8f0;
        color: #64748b;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div style="padding: 10px 5px 25px 5px;">
            <div style="font-size:38px;">🌾</div>
            <div style="font-size:24px;font-weight:800;color:#166534;">
                GovSchemeAI
            </div>
            <div style="font-size:14px;color:#64748b;">
                Government Scheme Assistant
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    st.markdown("### 🧭 Navigation")

    if st.button("🏠 Home", use_container_width=True):
        st.switch_page("app.py")

    if st.button("🤖 AI Chat", use_container_width=True):
        st.switch_page("pages/1_AI_Chat.py")

    if st.button("🔎 Find Schemes", use_container_width=True):
        st.switch_page("pages/2_Find_Schemes.py")

    if st.button("🎯 Eligibility", use_container_width=True):
        st.switch_page("pages/3_Eligibility.py")

    st.divider()

    st.info(
        "💡 Use AI Chat to ask questions about government schemes "
        "in simple language."
    )

# ============================================================
# HERO
# ============================================================

st.markdown(
    """
    <div class="hero">

        <div class="hero-badge">
            🇮🇳 Government Scheme Assistant
        </div>

        <h1>
            Find the right government scheme
            <span>for you.</span>
        </h1>

        <p>
            Discover government schemes, check eligibility,
            understand benefits and find where to apply —
            all in simple language.
        </p>

    </div>
    """,
    unsafe_allow_html=True
)

# ============================================================
# QUICK ACTIONS
# ============================================================

st.markdown(
    '<div class="section-title">What do you want to do?</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-subtitle">Choose an option to get started.</div>',
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3, gap="large")

with col1:

    st.markdown(
        """
        <div class="feature-card">

            <div class="feature-icon">🤖</div>

            <h3>AI Chat</h3>

            <p>
                Ask questions about government schemes
                in simple language and get AI-powered answers.
            </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button(
        "Open AI Chat →",
        key="open_ai",
        use_container_width=True
    ):
        st.switch_page("pages/1_AI_Chat.py")


with col2:

    st.markdown(
        """
        <div class="feature-card">

            <div class="feature-icon">🔎</div>

            <h3>Find Schemes</h3>

            <p>
                Search government schemes by state,
                category, crop and your specific requirement.
            </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button(
        "Find Schemes →",
        key="find_schemes",
        use_container_width=True
    ):
        st.switch_page("pages/2_Find_Schemes.py")


with col3:

    st.markdown(
        """
        <div class="feature-card">

            <div class="feature-icon">🎯</div>

            <h3>Check Eligibility</h3>

            <p>
                Enter your farmer details and find out
                which schemes you may be eligible for.
            </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button(
        "Check Eligibility →",
        key="eligibility",
        use_container_width=True
    ):
        st.switch_page("pages/3_Eligibility.py")

# ============================================================
# PLATFORM STATISTICS
# ============================================================

st.markdown(
    '<div class="section-title">GovSchemeAI at a glance</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-subtitle">Your government scheme discovery platform.</div>',
    unsafe_allow_html=True
)

a, b, c, d = st.columns(4)

with a:
    st.markdown(
        """
        <div class="stat-card">
            <div class="stat-number">500+</div>
            <div class="stat-label">Government Schemes</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with b:
    st.markdown(
        """
        <div class="stat-card">
            <div class="stat-number">500</div>
            <div class="stat-label">RAG Documents</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c:
    st.markdown(
        """
        <div class="stat-card">
            <div class="stat-number">AI</div>
            <div class="stat-label">Powered Assistant</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with d:
    st.markdown(
        """
        <div class="stat-card">
            <div class="stat-number">24/7</div>
            <div class="stat-label">Available</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# ============================================================
# HOW IT WORKS
# ============================================================

st.markdown(
    '<div class="section-title">How GovSchemeAI works</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-subtitle">Three simple steps to find the right scheme.</div>',
    unsafe_allow_html=True
)

s1, s2, s3 = st.columns(3, gap="large")

with s1:
    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-icon">1️⃣</div>
            <h3>Tell us your need</h3>
            <p>
                Ask a question or provide your
                farming and personal requirements.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

with s2:
    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-icon">2️⃣</div>
            <h3>Find matching schemes</h3>
            <p>
                Our RAG system searches the
                government scheme database.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

with s3:
    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-icon">3️⃣</div>
            <h3>Understand your options</h3>
            <p>
                See benefits, eligibility,
                documents and application information.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">

        <div style="font-size:20px;font-weight:700;color:#166534;">
            🌾 GovSchemeAI
        </div>

        <div style="margin-top:8px;">
            Making government schemes easier to discover and understand.
        </div>

        <div style="margin-top:12px;font-size:13px;">
            Always verify scheme details on the official government
            website before applying.
        </div>

    </div>
    """,
    unsafe_allow_html=True
)