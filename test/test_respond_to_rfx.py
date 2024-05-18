import os
from openai import OpenAI
from qdrant_client import QdrantClient
from src.respond_to_rfx import respond_to_rfx


def test_respond_to_rfx():
    rfx_questions_excel = "test_data/rfx_files/rfp_test_en_1.xlsx"
    output_excel = "test_data/rfx_files/rfp_test_en_1_responses.xlsx"
    language = "en"

    openai_client = OpenAI()
    embeddings_model = "text-embedding-3-small"

    qdrant_api_key = os.getenv("QDRANT_API_KEY")
    qdrant_url = os.getenv("QDRANT_API_URL")
    qclient = QdrantClient(
        url=qdrant_url,
        api_key=qdrant_api_key,
        timeout=60,
    )

    collection_name = "r_r_questions_1"

    respond_to_rfx(
        rfx_questions_excel=rfx_questions_excel,
        language=language,
        output_excel=output_excel,
        qclient=qclient,
        collection_name=collection_name,
        openai_client=openai_client,
        embeddings_model=embeddings_model,
        verbose=True,
    )
