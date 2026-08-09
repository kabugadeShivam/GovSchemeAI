
from langchain_huggingface import HuggingFaceEmbeddings


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


def get_embedding_model():

    embeddings = HuggingFaceEmbeddings(
        model_name=MODEL_NAME
    )

    return embeddings


if __name__ == "__main__":

    print("Loading embedding model...")

    embeddings = get_embedding_model()

    print("Embedding model loaded successfully.")

    test_text = "Government scheme for farmers"

    vector = embeddings.embed_query(test_text)

    print("Vector size:", len(vector))
    print("First 5 values:", vector[:5])
