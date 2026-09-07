from functools import lru_cache
from pathlib import Path

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_PATH = str(BASE_DIR / "database")
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


@lru_cache(maxsize=1)
def get_embedding_model():
    """Load the embedding model once per Streamlit process."""
    return HuggingFaceEmbeddings(model_name=MODEL_NAME)


@lru_cache(maxsize=1)
def get_vector_database():
    """Open the persisted Chroma database once per Streamlit process."""
    return Chroma(
        persist_directory=DATABASE_PATH,
        embedding_function=get_embedding_model()
    )


def search_schemes(query, k=5):
    vector_db = get_vector_database()
    return vector_db.similarity_search_with_relevance_scores(query, k=k)


def filter_results(results, query):
    query_lower = query.lower()
    filtered = []

    irrigation_query = any(
        word in query_lower
        for word in [
            "irrigation", "drip", "sprinkler", "water pump",
            "solar pump", "water support"
        ]
    )

    for document, score in results:
        if irrigation_query:
            irrigation_required = ""
            for line in document.page_content.splitlines():
                if line.strip().startswith("Irrigation Required:"):
                    irrigation_required = line.split(":", 1)[1].strip().lower()
                    break

            category = str(document.metadata.get("category", "")).lower()
            if irrigation_required == "yes" or category == "irrigation":
                filtered.append((document, score))
        else:
            filtered.append((document, score))

    return filtered


if __name__ == "__main__":
    query = "What irrigation schemes are available for farmers in Maharashtra?"
    results = filter_results(search_schemes(query), query)
    print(f"Results after filtering: {len(results)}")
    for i, (document, score) in enumerate(results, start=1):
        print("=" * 60)
        print(f"RESULT {i} | Score: {score:.4f}")
        print(f"Scheme: {document.metadata.get('scheme_name')}")
        print(f"State: {document.metadata.get('state')}")
        print(f"Category: {document.metadata.get('category')}")
