import sys
import os
import requests

# ============================================================
# PROJECT ROOT
# ============================================================

ROOT_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)


# ============================================================
# RAG RETRIEVER
# ============================================================

from rag.retriever import search_schemes, filter_results


# ============================================================
# OLLAMA
# ============================================================

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"

MODEL_NAME = "gemma3:4b"


# ============================================================
# EXTRACT INFORMATION FROM RETRIEVER RESULT
# ============================================================

def extract_result(result):

    """
    Your current retriever returns tuples.

    This function safely handles:
        tuple
        dictionary
        string
    """

    document = ""
    metadata = {}
    score = None

    # --------------------------------------------------------
    # Tuple result
    # --------------------------------------------------------

    if isinstance(result, tuple):

        # Common structure:
        # (document, metadata, score)

        if len(result) >= 1:
            document = result[0]

        if len(result) >= 2:
            if isinstance(result[1], dict):
                metadata = result[1]

        if len(result) >= 3:
            score = result[2]

    # --------------------------------------------------------
    # Dictionary result
    # --------------------------------------------------------

    elif isinstance(result, dict):

        document = result.get(
            "document",
            result.get("text", "")
        )

        metadata = result.get(
            "metadata",
            {}
        )

        score = result.get(
            "score",
            result.get("relevance_score")
        )

    # --------------------------------------------------------
    # String result
    # --------------------------------------------------------

    elif isinstance(result, str):

        document = result

    # --------------------------------------------------------
    # Safety
    # --------------------------------------------------------

    if document is None:
        document = ""

    if metadata is None:
        metadata = {}

    if not isinstance(metadata, dict):
        metadata = {}

    return document, metadata, score


# ============================================================
# BUILD RAG CONTEXT
# ============================================================

def format_schemes(results):

    if not results:
        return "No relevant government schemes were found."

    context_parts = []

    for index, result in enumerate(results, start=1):

        document, metadata, score = extract_result(result)

        scheme_name = metadata.get(
            "scheme_name",
            "Not specified"
        )

        scheme_id = metadata.get(
            "scheme_id",
            "Not specified"
        )

        state = metadata.get(
            "state",
            "Not specified"
        )

        district = metadata.get(
            "district",
            "Not specified"
        )

        category = metadata.get(
            "category",
            "Not specified"
        )

        context = f"""
============================================================
SCHEME {index}
============================================================

Scheme Name:
{scheme_name}

Scheme ID:
{scheme_id}

State:
{state}

District:
{district}

Category:
{category}

Scheme Details:
{document}
"""

        context_parts.append(context)

    return "\n".join(context_parts)


# ============================================================
# ASK GEMMA
# ============================================================

def generate_answer(question, context):

    prompt = f"""
You are GovSchemeAI, an AI assistant for Indian government
schemes.

Your job is to help citizens and farmers understand government
schemes clearly.

IMPORTANT RULES:

1. Use ONLY the information provided in the Government Scheme
   Database below.

2. Do NOT invent scheme names.

3. Do NOT invent eligibility conditions.

4. Do NOT invent subsidy amounts.

5. Do NOT invent websites or application procedures.

6. If the database does not contain enough information, say:
   "The available database does not contain enough information
   to answer this completely."

7. Give a simple, concise and farmer-friendly answer.

8. When useful, show:
   - Scheme name
   - Scheme ID
   - Eligibility
   - Benefits
   - Subsidy
   - Required documents
   - Where to apply

9. If multiple schemes match, list them separately.

10. Do not include irrelevant schemes merely because they are
    semantically similar.

============================================================
GOVERNMENT SCHEME DATABASE
============================================================

{context}

============================================================
USER QUESTION
============================================================

{question}

============================================================
ANSWER
============================================================
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.2
            }
        },
        timeout=180
    )

    response.raise_for_status()

    data = response.json()

    answer = data.get("response", "")

    if not answer:
        return "Sorry, I could not generate an answer."

    return answer.strip()


# ============================================================
# MAIN AI FUNCTION
# ============================================================

def ask_ai(question):

    if not question or not question.strip():

        return "Please enter a question."

    # --------------------------------------------------------
    # SEARCH VECTOR DATABASE
    # --------------------------------------------------------

    results = search_schemes(
        question
    )

    # --------------------------------------------------------
    # APPLY YOUR EXISTING FILTER
    # --------------------------------------------------------

    try:

        filtered = filter_results(
            results,
            question
        )

        # Only replace results if filtering actually returned
        # something.

        if filtered:
            results = filtered

    except Exception:

        # Keep semantic search results if the existing filter
        # has a different function signature.

        pass

    # --------------------------------------------------------
    # BUILD CONTEXT
    # --------------------------------------------------------

    context = format_schemes(
        results
    )

    # --------------------------------------------------------
    # SEND CONTEXT TO GEMMA
    # --------------------------------------------------------

    answer = generate_answer(
        question,
        context
    )

    return answer


# ============================================================
# COMMAND LINE TEST
# ============================================================

if __name__ == "__main__":

    print()
    print("============================================================")
    print("GovSchemeAI - RAG AI TEST")
    print("============================================================")

    question = input(
        "\nQuestion:\n"
    )

    print(
        "\nSearching government scheme database..."
    )

    try:

        answer = ask_ai(
            question
        )

        print()
        print("============================================================")
        print("AI ANSWER")
        print("============================================================")
        print()

        print(answer)

        print()
        print("============================================================")

    except requests.exceptions.ConnectionError:

        print()
        print("ERROR: Ollama is not reachable.")
        print()
        print("Make sure Ollama is running.")
        print("Your Gemma model is:")
        print("gemma3:4b")

    except Exception as e:

        print()
        print("ERROR:")
        print(type(e).__name__)
        print(str(e))