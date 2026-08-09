import streamlit as st
import pandas as pd
import os

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Find Government Schemes",
    page_icon="🔎",
    layout="wide"
)

# ============================================================
# PATH
# ============================================================

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

CSV_PATH = os.path.join(
    BASE_DIR,
    "data",
    "government_schemes.csv"
)

# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    df = pd.read_csv(CSV_PATH)

    # Replace missing values
    df = df.fillna("Not specified")

    return df


try:
    df = load_data()

except Exception as e:

    st.error("Unable to load the government schemes database.")
    st.code(str(e))
    st.stop()


# ============================================================
# HEADER
# ============================================================

st.title("🔎 Find Government Schemes")

st.write(
    "Find schemes based on your location, farming needs, "
    "category and other requirements."
)

st.divider()


# ============================================================
# SEARCH
# ============================================================

search = st.text_input(
    "🔍 Search schemes",
    placeholder="Example: irrigation, farmer subsidy, solar pump..."
)


# ============================================================
# FILTERS
# ============================================================

st.subheader("🎯 Filter Schemes")

col1, col2, col3 = st.columns(3)


# ------------------------------------------------------------
# STATE
# ------------------------------------------------------------

with col1:

    states = sorted(
        df["State"].astype(str).unique()
    )

    state = st.selectbox(
        "📍 State",
        ["All States"] + states
    )


# ------------------------------------------------------------
# DISTRICT
# ------------------------------------------------------------

with col2:

    if state != "All States":

        district_values = sorted(
            df[
                df["State"].astype(str) == state
            ]["District"].astype(str).unique()
        )

    else:

        district_values = sorted(
            df["District"].astype(str).unique()
        )

    district = st.selectbox(
        "🏙️ District",
        ["All Districts"] + district_values
    )


# ------------------------------------------------------------
# CATEGORY
# ------------------------------------------------------------

with col3:

    categories = sorted(
        df["Category"].astype(str).unique()
    )

    category = st.selectbox(
        "🏷️ Category",
        ["All Categories"] + categories
    )


# ============================================================
# SECOND ROW FILTERS
# ============================================================

col4, col5, col6 = st.columns(3)


# ------------------------------------------------------------
# CROP
# ------------------------------------------------------------

with col4:

    crops = sorted(
        df["Crop"].astype(str).unique()
    )

    crop = st.selectbox(
        "🌾 Crop",
        ["All Crops"] + crops
    )


# ------------------------------------------------------------
# GENDER
# ------------------------------------------------------------

with col5:

    genders = sorted(
        df["Gender"].astype(str).unique()
    )

    gender = st.selectbox(
        "👤 Gender",
        ["All"] + genders
    )


# ------------------------------------------------------------
# FPO
# ------------------------------------------------------------

with col6:

    fpo = st.selectbox(
        "🤝 FPO Requirement",
        [
            "All",
            "Yes",
            "No"
        ]
    )


st.write("")


# ============================================================
# SEARCH BUTTON
# ============================================================

search_button = st.button(
    "🔎 Find Matching Schemes",
    type="primary",
    use_container_width=True
)


# ============================================================
# FILTER FUNCTION
# ============================================================

def filter_schemes(data):

    results = data.copy()

    # --------------------------------------------------------
    # TEXT SEARCH
    # --------------------------------------------------------

    if search:

        search_text = search.lower()

        searchable_columns = [
            "Scheme_Name",
            "Category",
            "State",
            "District",
            "Crop",
            "Need",
            "Eligibility",
            "Benefit",
            "Keywords"
        ]

        mask = False

        for column in searchable_columns:

            if column in results.columns:

                mask = mask | results[column].astype(
                    str
                ).str.lower().str.contains(
                    search_text,
                    na=False,
                    regex=False
                )

        results = results[mask]

    # --------------------------------------------------------
    # STATE
    # --------------------------------------------------------

    if state != "All States":

        results = results[
            results["State"].astype(str) == state
        ]

    # --------------------------------------------------------
    # DISTRICT
    # --------------------------------------------------------

    if district != "All Districts":

        results = results[
            results["District"].astype(str) == district
        ]

    # --------------------------------------------------------
    # CATEGORY
    # --------------------------------------------------------

    if category != "All Categories":

        results = results[
            results["Category"].astype(str) == category
        ]

    # --------------------------------------------------------
    # CROP
    # --------------------------------------------------------

    if crop != "All Crops":

        results = results[
            results["Crop"].astype(str) == crop
        ]

    # --------------------------------------------------------
    # GENDER
    # --------------------------------------------------------

    if gender != "All":

        results = results[
            results["Gender"].astype(str) == gender
        ]

    # --------------------------------------------------------
    # FPO
    # --------------------------------------------------------

    if fpo != "All":

        results = results[
            results["FPO_Required"].astype(str) == fpo
        ]

    return results


# ============================================================
# RESULTS
# ============================================================

if search_button:

    results = filter_schemes(df)

    st.divider()

    st.subheader(
        f"📋 {len(results)} Scheme(s) Found"
    )

    # --------------------------------------------------------
    # NO RESULTS
    # --------------------------------------------------------

    if len(results) == 0:

        st.warning(
            "No schemes match your selected criteria."
        )

        st.info(
            "Try removing one or more filters."
        )

    # --------------------------------------------------------
    # RESULTS
    # --------------------------------------------------------

    else:

        for _, scheme in results.iterrows():

            with st.container(border=True):

                st.markdown(
                    f"### 🌾 {scheme['Scheme_Name']}"
                )

                st.caption(
                    f"Scheme ID: {scheme['Scheme_ID']}"
                )

                # ------------------------------------------------
                # BASIC INFO
                # ------------------------------------------------

                c1, c2, c3, c4 = st.columns(4)

                with c1:
                    st.markdown(
                        f"**📍 State**  \n"
                        f"{scheme['State']}"
                    )

                with c2:
                    st.markdown(
                        f"**🏙️ District**  \n"
                        f"{scheme['District']}"
                    )

                with c3:
                    st.markdown(
                        f"**🏷️ Category**  \n"
                        f"{scheme['Category']}"
                    )

                with c4:
                    st.markdown(
                        f"**🌾 Crop**  \n"
                        f"{scheme['Crop']}"
                    )

                st.divider()

                # ------------------------------------------------
                # BENEFIT
                # ------------------------------------------------

                st.markdown("**💰 Benefit**")

                st.write(
                    scheme["Benefit"]
                )

                # ------------------------------------------------
                # SUBSIDY
                # ------------------------------------------------

                st.markdown("**💵 Subsidy / Financial Support**")

                st.write(
                    scheme["Subsidy"]
                )

                # ------------------------------------------------
                # ELIGIBILITY
                # ------------------------------------------------

                st.markdown("**✅ Eligibility**")

                st.write(
                    scheme["Eligibility"]
                )

                # ------------------------------------------------
                # APPLICATION
                # ------------------------------------------------

                c5, c6 = st.columns(2)

                with c5:

                    st.markdown(
                        "**📄 Required Documents**"
                    )

                    st.write(
                        scheme["Required_Documents"]
                    )

                with c6:

                    st.markdown(
                        "**🏢 Apply At**"
                    )

                    st.write(
                        scheme["Apply_At"]
                    )

                # ------------------------------------------------
                # WEBSITE
                # ------------------------------------------------

                website = str(
                    scheme["Official_Website"]
                )

                if website != "Not specified":

                    st.link_button(
                        "🌐 Official Website",
                        website
                    )