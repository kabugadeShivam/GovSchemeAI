
import pandas as pd
from langchain_core.documents import Document


CSV_PATH = "data/government_schemes.csv"


def load_schemes():
    """Load government schemes from CSV."""

    df = pd.read_csv(CSV_PATH)

    print(f"Total Schemes: {len(df)}")

    return df


def create_documents(df):
    """Convert each CSV row into a LangChain Document."""

    documents = []

    for _, row in df.iterrows():

        content = f"""
Scheme Name: {row['Scheme_Name']}

Scheme ID: {row['Scheme_ID']}

Type: {row['Type']}

State: {row['State']}

District: {row['District']}

Category: {row['Category']}

Crop: {row['Crop']}

Need: {row['Need']}

Eligibility: {row['Eligibility']}

Benefits: {row['Benefit']}

Subsidy: {row['Subsidy']}

Minimum Land Required: {row['Min_Land_Acres']} acres

Maximum Land Required: {row['Max_Land_Acres']} acres

Income Limit: {row['Income_Limit']}

Gender: {row['Gender']}

Minimum Age: {row['Age_Min']}

Maximum Age: {row['Age_Max']}

FPO Required: {row['FPO_Required']}

Organic Farming Required: {row['Organic_Required']}

Irrigation Required: {row['Irrigation_Required']}

Required Documents: {row['Required_Documents']}

Apply At: {row['Apply_At']}

Official Website: {row['Official_Website']}

Keywords: {row['Keywords']}
"""

        document = Document(
            page_content=content,
            metadata={
                "scheme_id": str(row["Scheme_ID"]),
                "scheme_name": str(row["Scheme_Name"]),
                "state": str(row["State"]),
                "category": str(row["Category"]),
            }
        )

        documents.append(document)

    print(f"Created Documents: {len(documents)}")

    return documents


if __name__ == "__main__":

    df = load_schemes()

    documents = create_documents(df)

    print("\nFirst Document:")
    print(documents[0].page_content)

    print("\nMetadata:")
    print(documents[0].metadata)

