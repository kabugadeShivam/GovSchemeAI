
from pathlib import Path

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings


# ==========================================
# PATHS
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATABASE_PATH = str(BASE_DIR / "database")


# ==========================================
# EMBEDDING MODEL
# ==========================================

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


# ==========================================
# GET VECTOR DATABASE
# ==========================================

def get_vector_database():

    embeddings = HuggingFaceEmbeddings(
        model_name=MODEL_NAME
    )

    vector_db = Chroma(
        persist_directory=DATABASE_PATH,
        embedding_function=embeddings
    )

    return vector_db


# ==========================================
# SEMANTIC SEARCH
# ==========================================

def search_schemes(query, k=5):

    vector_db = get_vector_database()

    results = vector_db.similarity_search_with_relevance_scores(
        query,
        k=k
    )

    return results


# ==========================================
# QUERY-AWARE FILTER
# ==========================================

def filter_results(results, query):

    query_lower = query.lower()

    filtered = []

    # --------------------------------------
    # Detect query type
    # --------------------------------------

    irrigation_query = any(
        word in query_lower
        for word in [
            "irrigation",
            "drip",
            "sprinkler",
            "water pump",
            "solar pump",
            "water support"
        ]
    )

    # --------------------------------------
    # Process results
    # --------------------------------------

    for document, score in results:

        content = document.page_content

        # ----------------------------------
        # Irrigation filtering
        # ----------------------------------

        if irrigation_query:

            irrigation_required = ""

            for line in content.splitlines():

                if line.strip().startswith(
                    "Irrigation Required:"
                ):

                    irrigation_required = (
                        line.split(
                            ":",
                            1
                        )[1]
                        .strip()
                        .lower()
                    )

                    break

            category = str(
                document.metadata.get(
                    "category",
                    ""
                )
            ).lower()

            # Keep only schemes where:
            #
            # Irrigation Required = Yes
            #
            # OR category = Irrigation

            if (
                irrigation_required == "yes"
                or category == "irrigation"
            ):

                filtered.append(
                    (document, score)
                )

        else:

            filtered.append(
                (document, score)
            )

    return filtered


# ==========================================
# TEST
# ==========================================

if __name__ == "__main__":

    query = (
        "What irrigation schemes are available "
        "for farmers in Maharashtra?"
    )

    print("Searching...\n")

    results = search_schemes(query)

    print(
        f"Semantic results: {len(results)}\n"
    )

    filtered_results = filter_results(
        results,
        query
    )

    print(
        f"Results after filtering: "
        f"{len(filtered_results)}\n"
    )

    for i, (document, score) in enumerate(
        filtered_results,
        start=1
    ):

        print("=" * 60)

        print(f"RESULT {i}")

        print("=" * 60)

        print(
            f"Relevance Score: "
            f"{score:.4f}"
        )

        print(
            f"Scheme: "
            f"{document.metadata.get('scheme_name')}"
        )

        print(
            f"State: "
            f"{document.metadata.get('state')}"
        )

        print(
            f"Category: "
            f"{document.metadata.get('category')}"
        )

        print()

