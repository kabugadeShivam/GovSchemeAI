import os
import re
import requests
import streamlit as st

st.set_page_config(page_title="AI Assistant | GovSchemeAI", page_icon="🤖", layout="wide")

try:
    from rag.retriever import search_schemes, filter_results
except Exception as e:
    st.error("Could not load the RAG system.")
    st.code(str(e))
    st.stop()

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
OLLAMA_MODEL = "gemma3:4b"
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "llama-3.1-8b-instant"

if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant",
        "content": "Namaste! 👋 Ask me about government schemes, eligibility, subsidies, documents or where to apply."
    }]

st.title("🤖 GovSchemeAI Assistant")
st.write("Ask questions about government schemes in simple language.")
st.divider()

q1, q2, q3, q4 = st.columns(4)
examples = [
    "What irrigation schemes are available for farmers in Maharashtra?",
    "What agricultural subsidy schemes are available?",
    "What documents are generally required to apply for agricultural schemes?",
    "Which government schemes can benefit farmers?"
]
for col, label, question in zip(
    [q1, q2, q3, q4],
    ["🌾 Irrigation schemes", "💰 Subsidy schemes", "📄 Required documents", "👨‍🌾 Farmer schemes"],
    examples
):
    with col:
        if st.button(label, use_container_width=True):
            st.session_state.pending_question = question

st.divider()
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

question = st.chat_input("Ask about government schemes...")
if st.session_state.get("pending_question"):
    question = st.session_state.pop("pending_question")


def extract_field(text, field_names):
    for field in field_names:
        match = re.search(rf"{re.escape(field)}:\s*(.*)", text, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    return "Not specified"


def build_context(results):
    context = []
    cards = []
    for document, score in results:
        text = document.page_content
        card = {
            "name": extract_field(text, ["Scheme Name"]),
            "id": extract_field(text, ["Scheme ID"]),
            "state": extract_field(text, ["State"]),
            "district": extract_field(text, ["District"]),
            "category": extract_field(text, ["Category"]),
            "crop": extract_field(text, ["Crop"]),
            "eligibility": extract_field(text, ["Eligibility"]),
            "benefit": extract_field(text, ["Benefits", "Benefit"]),
            "subsidy": extract_field(text, ["Subsidy"]),
            "documents": extract_field(text, ["Required Documents"]),
            "apply_at": extract_field(text, ["Apply At"]),
            "website": extract_field(text, ["Official Website"]),
        }
        cards.append(card)
        context.append(text)
    return "\n\n---\n\n".join(context), cards


def generate_cloud_answer(question, context):
    api_key = st.secrets.get("GROQ_API_KEY", os.getenv("GROQ_API_KEY", ""))
    if not api_key:
        return None
    prompt = f"""You are GovSchemeAI, a helpful Indian government scheme assistant.
Answer ONLY from the government scheme information below. Do not invent facts.
Use simple language. Mention the most relevant schemes first and include eligibility, benefit, subsidy, documents and where to apply when available.

Question: {question}

Government scheme information:
{context}

End with: Please verify the latest details on the official government website before applying."""
    response = requests.post(
        GROQ_URL,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={"model": GROQ_MODEL, "messages": [{"role": "user", "content": prompt}], "temperature": 0.2},
        timeout=90
    )
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"].strip()


def generate_local_answer(question, context):
    try:
        response = requests.post(
            OLLAMA_URL,
            json={"model": OLLAMA_MODEL, "prompt": f"Answer using only this data.\n\nQuestion: {question}\n\nData:\n{context}", "stream": False},
            timeout=90
        )
        response.raise_for_status()
        return response.json().get("response", "").strip()
    except Exception:
        return None


def fallback_answer(cards):
    lines = ["### Matching government schemes", ""]
    for card in cards[:5]:
        lines.append(f"**{card['name']}**")
        lines.append(f"- Eligibility: {card['eligibility']}")
        lines.append(f"- Benefit: {card['benefit']}")
        lines.append(f"- Subsidy: {card['subsidy']}")
        lines.append(f"- Apply at: {card['apply_at']}")
        lines.append("")
    lines.append("Please verify the latest details on the official government website before applying.")
    return "\n".join(lines)


if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        try:
            with st.spinner("🔎 Searching government schemes..."):
                results = filter_results(search_schemes(question, k=8), question)

            if not results:
                answer = "I couldn't find a matching scheme in the current database. Try mentioning your state, district, crop or requirement."
                st.warning(answer)
            else:
                context, cards = build_context(results)
                answer = None

                # Streamlit Cloud: use Groq when GROQ_API_KEY is configured.
                # Local development: use Ollama when it is running.
                try:
                    answer = generate_cloud_answer(question, context)
                except Exception:
                    answer = None

                if not answer:
                    answer = generate_local_answer(question, context)

                if not answer:
                    answer = fallback_answer(cards)
                    st.info("AI model is not configured, so GovSchemeAI is showing the verified scheme information retrieved from its database.")

                st.markdown(answer)
                st.divider()
                st.markdown("### 📚 Sources from GovSchemeAI database")

                for card in cards:
                    with st.expander(f"📋 {card['name']}"):
                        st.caption(f"Scheme ID: {card['id']}")
                        c1, c2 = st.columns(2)
                        with c1:
                            st.markdown(f"**📍 Location**  \n{card['state']} — {card['district']}")
                            st.markdown(f"**🌾 Crop**  \n{card['crop']}")
                            st.markdown(f"**🏷️ Category**  \n{card['category']}")
                        with c2:
                            st.markdown(f"**💰 Benefit**  \n{card['benefit']}")
                            st.markdown(f"**💵 Subsidy**  \n{card['subsidy']}")
                            st.markdown(f"**🏢 Apply At**  \n{card['apply_at']}")
                        st.markdown(f"**📄 Documents:** {card['documents']}")
                        if card["website"].startswith("http"):
                            st.link_button("🌐 Official Website", card["website"])

            st.session_state.messages.append({"role": "assistant", "content": answer})

        except Exception as e:
            st.error("Something went wrong while processing your question.")
            st.code(str(e))

st.divider()
if st.button("🗑️ Clear conversation"):
    st.session_state.messages = [{
        "role": "assistant",
        "content": "Namaste! 👋 Ask me about government schemes, eligibility, subsidies, documents or where to apply."
    }]
    st.rerun()
