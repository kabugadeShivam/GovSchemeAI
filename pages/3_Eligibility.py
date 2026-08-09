import streamlit as st
import pandas as pd
import os

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Check Eligibility",
    page_icon="🎯",
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
# LOAD DATABASE
# ============================================================

@st.cache_data
def load_data():

    df = pd.read_csv(CSV_PATH)

    df = df.fillna("Not specified")

    return df


try:

    df = load_data()

except Exception as e:

    st.error("Unable to load the government scheme database.")
    st.code(str(e))
    st.stop()


# ============================================================
# HEADER
# ============================================================

st.title("🎯 Check Your Eligibility")

st.write(
    "Enter your basic details and GovSchemeAI will find "
    "schemes that may be suitable for you."
)

st.info(
    "💡 This is an initial eligibility check. "
    "Always verify the final eligibility requirements "
    "on the official government website."
)

st.divider()


# ============================================================
# FARMER PROFILE
# ============================================================

st.subheader("👨‍🌾 Tell us about yourself")

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
        states
    )


# ------------------------------------------------------------
# DISTRICT
# ------------------------------------------------------------

with col2:

    districts = sorted(
        df[
            df["State"].astype(str) == state
        ]["District"].astype(str).unique()
    )

    district = st.selectbox(
        "🏙️ District",
        districts
    )


# ------------------------------------------------------------
# AGE
# ------------------------------------------------------------

with col3:

    age = st.number_input(
        "🎂 Age",
        min_value=1,
        max_value=120,
        value=25
    )


# ============================================================
# SECOND ROW
# ============================================================

col4, col5, col6 = st.columns(3)

# ------------------------------------------------------------
# GENDER
# ------------------------------------------------------------

with col4:

    gender = st.selectbox(
        "👤 Gender",
        [
            "Male",
            "Female",
            "Other"
        ]
    )


# ------------------------------------------------------------
# LAND
# ------------------------------------------------------------

with col5:

    land = st.number_input(
        "🌾 Land holding (acres)",
        min_value=0.0,
        max_value=1000.0,
        value=2.0,
        step=0.5
    )


# ------------------------------------------------------------
# CROP
# ------------------------------------------------------------

with col6:

    crops = sorted(
        df["Crop"].astype(str).unique()
    )

    crop = st.selectbox(
        "🌱 Crop",
        crops
    )


# ============================================================
# THIRD ROW
# ============================================================

col7, col8, col9 = st.columns(3)

# ------------------------------------------------------------
# INCOME
# ------------------------------------------------------------

with col7:

    income = st.number_input(
        "💰 Annual family income (₹)",
        min_value=0,
        max_value=100000000,
        value=300000,
        step=10000
    )


# ------------------------------------------------------------
# FPO
# ------------------------------------------------------------

with col8:

    fpo_member = st.selectbox(
        "🤝 Member of FPO / Cooperative?",
        [
            "Yes",
            "No"
        ]
    )


# ------------------------------------------------------------
# ORGANIC
# ------------------------------------------------------------

with col9:

    organic = st.selectbox(
        "🌱 Organic farming?",
        [
            "Yes",
            "No"
        ]
    )


# ============================================================
# IRRIGATION
# ============================================================

irrigation = st.selectbox(
    "💧 Do you have irrigation facilities?",
    [
        "Yes",
        "No"
    ]
)


st.write("")


# ============================================================
# CHECK BUTTON
# ============================================================

check_button = st.button(
    "🎯 Check My Eligibility",
    type="primary",
    use_container_width=True
)


# ============================================================
# ELIGIBILITY FUNCTION
# ============================================================

def check_scheme_eligibility(scheme):

    reasons = []

    # --------------------------------------------------------
    # STATE
    # --------------------------------------------------------

    if str(scheme["State"]).lower() != str(state).lower():

        return False, [
            f"Scheme is available in {scheme['State']}."
        ]


    # --------------------------------------------------------
    # DISTRICT
    # --------------------------------------------------------

    scheme_district = str(
        scheme["District"]
    ).strip().lower()

    if (
        scheme_district != "not specified"
        and scheme_district != "all"
        and scheme_district != str(district).strip().lower()
    ):

        return False, [
            f"Scheme is listed for {scheme['District']}."
        ]


    # --------------------------------------------------------
    # CROP
    # --------------------------------------------------------

    scheme_crop = str(
        scheme["Crop"]
    ).strip().lower()

    if (
        scheme_crop != "not specified"
        and scheme_crop != "all"
        and scheme_crop != "general"
        and scheme_crop != str(crop).strip().lower()
    ):

        return False, [
            f"Scheme is intended for {scheme['Crop']}."
        ]


    # --------------------------------------------------------
    # AGE
    # --------------------------------------------------------

    try:

        age_min = float(
            scheme["Age_Min"]
        )

        age_max = float(
            scheme["Age_Max"]
        )

        if age < age_min:

            return False, [
                f"Minimum age is {int(age_min)}."
            ]

        if age > age_max:

            return False, [
                f"Maximum age is {int(age_max)}."
            ]

    except:

        pass


    # --------------------------------------------------------
    # LAND
    # --------------------------------------------------------

    try:

        min_land = float(
            scheme["Min_Land_Acres"]
        )

        max_land = float(
            scheme["Max_Land_Acres"]
        )

        if land < min_land:

            return False, [
                f"Minimum land requirement is "
                f"{min_land} acres."
            ]

        if land > max_land:

            return False, [
                f"Maximum land limit is "
                f"{max_land} acres."
            ]

    except:

        pass


    # --------------------------------------------------------
    # GENDER
    # --------------------------------------------------------

    scheme_gender = str(
        scheme["Gender"]
    ).strip().lower()

    if scheme_gender not in [
        "all",
        "not specified",
        "nan"
    ]:

        if scheme_gender != gender.lower():

            return False, [
                f"This scheme is for "
                f"{scheme['Gender']} applicants."
            ]


    # --------------------------------------------------------
    # INCOME
    # --------------------------------------------------------

    income_limit = str(
        scheme["Income_Limit"]
    ).strip().lower()

    if (
        income_limit
        and income_limit not in [
            "not specified",
            "nan",
            "none"
        ]
    ):

        try:

            import re

            numbers = re.findall(
                r"[\d,.]+",
                income_limit
            )

            if numbers:

                limit = float(
                    numbers[0].replace(",", "")
                )

                # Convert lakh values
                if "lakh" in income_limit:

                    limit = limit * 100000

                if income > limit:

                    return False, [
                        f"Income limit is "
                        f"{scheme['Income_Limit']}."
                    ]

        except:

            pass


    # --------------------------------------------------------
    # FPO
    # --------------------------------------------------------

    fpo_required = str(
        scheme["FPO_Required"]
    ).strip().lower()

    if fpo_required == "yes" and fpo_member != "Yes":

        return False, [
            "Membership of an FPO / Cooperative is required."
        ]


    # --------------------------------------------------------
    # ORGANIC
    # --------------------------------------------------------

    organic_required = str(
        scheme["Organic_Required"]
    ).strip().lower()

    if organic_required == "yes" and organic != "Yes":

        return False, [
            "Organic farming is required."
        ]


    # --------------------------------------------------------
    # IRRIGATION
    # --------------------------------------------------------

    irrigation_required = str(
        scheme["Irrigation_Required"]
    ).strip().lower()

    if (
        irrigation_required == "yes"
        and irrigation != "Yes"
    ):

        return False, [
            "Irrigation facility is required."
        ]


    # --------------------------------------------------------
    # ELIGIBLE
    # --------------------------------------------------------

    reasons.append(
        "Your basic details match the available "
        "eligibility conditions."
    )

    return True, reasons


# ============================================================
# RUN ELIGIBILITY CHECK
# ============================================================

if check_button:

    st.divider()

    st.subheader("📋 Eligibility Results")

    eligible_schemes = []
    rejected_schemes = []

    # --------------------------------------------------------
    # CHECK EACH SCHEME
    # --------------------------------------------------------

    for _, scheme in df.iterrows():

        eligible, reasons = check_scheme_eligibility(
            scheme
        )

        if eligible:

            eligible_schemes.append(
                (scheme, reasons)
            )

        else:

            rejected_schemes.append(
                (scheme, reasons)
            )


    # ========================================================
    # RESULTS
    # ========================================================

    if eligible_schemes:

        st.success(
            f"🎉 We found {len(eligible_schemes)} "
            f"scheme(s) that may match your profile."
        )

        for scheme, reasons in eligible_schemes:

            with st.container(border=True):

                st.markdown(
                    f"### ✅ {scheme['Scheme_Name']}"
                )

                st.caption(
                    f"Scheme ID: {scheme['Scheme_ID']}"
                )

                c1, c2, c3 = st.columns(3)

                with c1:

                    st.markdown(
                        f"**📍 Location**  \n"
                        f"{scheme['State']} — "
                        f"{scheme['District']}"
                    )

                with c2:

                    st.markdown(
                        f"**🌾 Crop**  \n"
                        f"{scheme['Crop']}"
                    )

                with c3:

                    st.markdown(
                        f"**🏷️ Category**  \n"
                        f"{scheme['Category']}"
                    )

                st.divider()

                st.markdown("**💰 Benefit**")

                st.write(
                    scheme["Benefit"]
                )

                st.markdown("**💵 Subsidy / Support**")

                st.write(
                    scheme["Subsidy"]
                )

                st.markdown("**📄 Required Documents**")

                st.write(
                    scheme["Required_Documents"]
                )

                st.markdown("**🏢 Apply At**")

                st.write(
                    scheme["Apply_At"]
                )

                website = str(
                    scheme["Official_Website"]
                )

                if website != "Not specified":

                    st.link_button(
                        "🌐 Official Website",
                        website
                    )

    else:

        st.warning(
            "No schemes matched all the basic eligibility "
            "conditions you entered."
        )

        st.info(
            "💡 Try changing your crop, district, land "
            "holding or other details."
        )


# ============================================================
# DISCLAIMER
# ============================================================

st.divider()

st.caption(
    "⚠️ Eligibility shown here is an initial screening "
    "based on the information available in GovSchemeAI. "
    "Final eligibility is determined by the concerned "
    "government department."
)