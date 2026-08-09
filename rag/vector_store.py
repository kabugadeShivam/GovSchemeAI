
from pathlib import Path

from langchain_chroma import Chroma

from loader import load_schemes, create_documents
from embeddings import get_embedding_model


# Project root
BASE_DIR = Path(__file__).resolve().parent.parent

# Chroma database location
DATABASE_PATH = str(BASE_DIR / "database")


def create_vector_database():

    print("Loading government schemes...")

    df = load_schemes()

    print("Creating documents...")

    documents = create_documents(df)

    print("Loading embedding model...")

    embeddings = get_embedding_model()

    print("Creating ChromaDB...")

    vector_db = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=DATABASE_PATH
    )

    print("\nVector database created successfully!")

    print(f"Total documents stored: {len(documents)}")

    return vector_db


if __name__ == "__main__":

    create_vector_database()

