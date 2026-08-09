import streamlit as st
import sys
import os
import requests

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AI Assistant | GovSchemeAI",
    page_icon="🤖",
    layout="wide"
)

# ============================================================
# PROJECT PATH
# ============================================================

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# ============================================================
# RAG IMPORT
# ============================================================

try:
    from rag.retriever import search_schemes, filter_results
except Exception as e:
    st.error("Could not load the RAG system.")
    st.code(str(e))
    st.stop()

# ============================================================
# OLLAMA
# ============================================================

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
MODEL_NAME = "gemma3:4b"


# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:

    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Namaste! 👋 I am GovSchemeAI.\n\n"
                "Ask me about government schemes, eligibility, "
                "subsidies, documents or where to apply."
            )
        }
    ]


# ============================================================
# HEADER
# ============================================================

st.title("🤖 GovSchemeAI Assistant")

st.write(
    "Ask questions about government schemes in simple language."
)

st.divider()


# ============================================================
# EXAMPLE QUESTIONS
# ============================================================

st.markdown("### 💡 Try asking")

q1, q2, q3, q4 = st.columns(4)

with q1:

    if st.button(
        "🌾 Irrigation schemes",
        use_container_width=True
    ):

        st.session_state.pending_question = (
            "What irrigation schemes are available "
            "for farmers in Maharashtra?"
        )


with q2:

    if st.button(
        "💰 Subsidy schemes",
        use_container_width=True
    ):

        st.session_state.pending_question = (
            "What agricultural subsidy schemes "
            "are available?"
        )


with q3:

    if st.button(
        "📄 Required documents",
        use_container_width=True
    ):

        st.session_state.pending_question = (
            "What documents are generally required "
            "to apply for agricultural schemes?"
        )


with q4:

    if st.button(
        "👨‍🌾 Farmer schemes",
        use_container_width=True
    ):

        st.session_state.pending_question = (
            "Which government schemes can benefit farmers?"
        )


st.divider()


# ============================================================
# DISPLAY CHAT HISTORY
# ============================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(
            message["content"]
        )


# ============================================================
# QUESTION
# ============================================================

question = st.chat_input(
    "Ask about government schemes..."
)


# Handle example button

if (
    "pending_question" in st.session_state
    and st.session_state.pending_question
):

    question = st.session_state.pending_question

    st.session_state.pending_question = None


# ============================================================
# PROCESS QUESTION
# ============================================================

if question:

    # --------------------------------------------------------
    # USER MESSAGE
    # --------------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message("user"):

        st.markdown(question)


    # --------------------------------------------------------
    # ASSISTANT
    # --------------------------------------------------------

    with st.chat_message("assistant"):

        with st.spinner(
            "🔎 Searching government schemes..."
        ):

            try:

                # ====================================================
                # RAG SEARCH
                # ====================================================

                results = search_schemes(
                    question
                )

                # ====================================================
                # FILTER RESULTS
                # ====================================================

                try:

                    results = filter_results(
                        results,
                        question
                    )

                except TypeError:

                    # If your current filter_results
                    # accepts only one argument
                    pass


                # ====================================================
                # CHECK RESULTS
                # ====================================================

                if not results:

                    answer = (
                        "I couldn't find a matching scheme "
                        "in the current government scheme database.\n\n"
                        "Try mentioning your **state, district, "
                        "crop or requirement**."
                    )

                    st.markdown(answer)

                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": answer
                        }
                    )

                    st.stop()


                # ====================================================
                # PREPARE CONTEXT
                # ====================================================

                context_parts = []

                scheme_cards = []


                for item in results:

                    # ------------------------------------------------
                    # HANDLE DIFFERENT RESULT FORMATS
                    # ------------------------------------------------

                    if isinstance(item, tuple):

                        if len(item) >= 2:

                            score = item[0]
                            scheme = item[1]

                        else:

                            score = 0
                            scheme = item[0]

                    elif isinstance(item, dict):

                        score = item.get(
                            "score",
                            0
                        )

                        scheme = item

                    else:

                        continue


                    # ------------------------------------------------
                    # NORMALIZE SCHEME
                    # ------------------------------------------------

                    if hasattr(
                        scheme,
                        "get"
                    ):

                        name = scheme.get(
                            "Scheme_Name",
                            scheme.get(
                                "scheme_name",
                                "Unknown scheme"
                            )
                        )

                        scheme_id = scheme.get(
                            "Scheme_ID",
                            scheme.get(
                                "scheme_id",
                                ""
                            )
                        )

                        state = scheme.get(
                            "State",
                            scheme.get(
                                "state",
                                ""
                            )
                        )

                        district = scheme.get(
                            "District",
                            scheme.get(
                                "district",
                                ""
                            )
                        )

                        category = scheme.get(
                            "Category",
                            scheme.get(
                                "category",
                                ""
                            )
                        )

                        crop = scheme.get(
                            "Crop",
                            scheme.get(
                                "crop",
                                ""
                            )
                        )

                        eligibility = scheme.get(
                            "Eligibility",
                            ""
                        )

                        benefit = scheme.get(
                            "Benefit",
                            scheme.get(
                                "Benefits",
                                ""
                            )
                        )

                        subsidy = scheme.get(
                            "Subsidy",
                            ""
                        )

                        documents = scheme.get(
                            "Required_Documents",
                            ""
                        )

                        apply_at = scheme.get(
                            "Apply_At",
                            ""
                        )

                        website = scheme.get(
                            "Official_Website",
                            ""
                        )

                    else:

                        continue


                    # ------------------------------------------------
                    # CONTEXT
                    # ------------------------------------------------

                    context_parts.append(
                        f"""
SCHEME:
{name}

Scheme ID:
{scheme_id}

State:
{state}

District:
{district}

Category:
{category}

Crop:
{crop}

Eligibility:
{eligibility}

Benefit:
{benefit}

Subsidy:
{subsidy}

Required Documents:
{documents}

Apply At:
{apply_at}

Official Website:
{website}
"""
                    )


                    scheme_cards.append(
                        {
                            "name": name,
                            "id": scheme_id,
                            "state": state,
                            "district": district,
                            "category": category,
                            "crop": crop,
                            "eligibility": eligibility,
                            "benefit": benefit,
                            "subsidy": subsidy,
                            "documents": documents,
                            "apply_at": apply_at,
                            "website": website
                        }
                    )


                context = "\n".join(
                    context_parts
                )


                # ====================================================
                # PROMPT
                # ====================================================

                prompt = f"""
You are GovSchemeAI, a helpful Indian government scheme assistant.

Answer the farmer's question using ONLY the government scheme
information provided below.

Do not invent schemes, benefits, eligibility conditions,
subsidies, documents or websites.

If the information is not available, clearly say so.

Use simple language suitable for a farmer.

Question:
{question}

Government scheme information:
{context}

Instructions:

1. Answer the question directly.
2. Mention the most relevant schemes first.
3. For each relevant scheme mention:
   - Scheme name
   - Eligibility
   - Benefit
   - Subsidy
   - Documents
   - Where to apply
4. Do not include unrelated schemes.
5. Do not make assumptions.
6. Keep the answer concise and readable.
7. End with:
"Please verify the latest details on the official government website before applying."
"""


                # ====================================================
                # OLLAMA REQUEST
                # ====================================================

                response = requests.post(
                    OLLAMA_URL,
                    json={
                        "model": MODEL_NAME,
                        "prompt": prompt,
                        "stream": False
                    },
                    timeout=180
                )


                response.raise_for_status()


                data = response.json()


                answer = data.get(
                    "response",
                    ""
                ).strip()


                if not answer:

                    answer = (
                        "I could not generate an answer. "
                        "Please try again."
                    )


                # ====================================================
                # SHOW ANSWER
                # ====================================================

                st.markdown(answer)


                # ====================================================
                # SOURCE SCHEMES
                # ====================================================

                st.divider()

                st.markdown(
                    "### 📚 Sources from GovSchemeAI database"
                )


                for card in scheme_cards:

                    with st.expander(
                        f"📋 {card['name']}"
                    ):

                        st.caption(
                            f"Scheme ID: {card['id']}"
                        )

                        c1, c2 = st.columns(2)


                        with c1:

                            st.markdown(
                                f"**📍 Location**  \n"
                                f"{card['state']} — "
                                f"{card['district']}"
                            )

                            st.markdown(
                                f"**🌾 Crop**  \n"
                                f"{card['crop']}"
                            )

                            st.markdown(
                                f"**🏷️ Category**  \n"
                                f"{card['category']}"
                            )


                        with c2:

                            st.markdown(
                                f"**💰 Benefit**  \n"
                                f"{card['benefit']}"
                            )

                            st.markdown(
                                f"**💵 Subsidy**  \n"
                                f"{card['subsidy']}"
                            )

                            st.markdown(
                                f"**🏢 Apply At**  \n"
                                f"{card['apply_at']}"
                            )


                        if card["documents"]:

                            st.markdown(
                                f"**📄 Documents:** "
                                f"{card['documents']}"
                            )


                        website = str(
                            card["website"]
                        ).strip()


                        # Extract URL from markdown
                        if website.startswith("["):

                            match = __import__(
                                "re"
                            ).search(
                                r"\((.*?)\)",
                                website
                            )

                            if match:

                                website = match.group(1)


                        if website.startswith(
                            "http"
                        ):

                            st.link_button(
                                "🌐 Official Website",
                                website
                            )


                # ====================================================
                # SAVE ASSISTANT MESSAGE
                # ====================================================

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer
                    }
                )


            except requests.exceptions.ConnectionError:

                error_message = (
                    "❌ I can't connect to the local AI model.\n\n"
                    "Make sure Ollama is running and "
                    "`gemma3:4b` is available."
                )

                st.error(error_message)


            except requests.exceptions.Timeout:

                st.error(
                    "⏳ The AI model took too long to respond. "
                    "Please try the question again."
                )


            except Exception as e:

                st.error(
                    "Something went wrong while processing "
                    "your question."
                )

                st.code(
                    str(e)
                )


# ============================================================
# CLEAR CHAT
# ============================================================

st.divider()

if st.button(
    "🗑️ Clear conversation"
):

    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Namaste! 👋 I am GovSchemeAI.\n\n"
                "Ask me about government schemes, eligibility, "
                "subsidies, documents or where to apply."
            )
        }
    ]

    st.rerun()