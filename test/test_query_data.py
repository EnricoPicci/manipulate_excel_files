import os

from openai import OpenAI
from qdrant_client import QdrantClient

from src.query_data import search_answers


def test_search_answers():
    question = "Do you comply with GDPR and other local EU Data Protection regulations?"
    language = "en"

    collection_name = "r_r_questions_1"

    client = OpenAI()
    model = "text-embedding-3-small"

    qdrant_api_key = os.getenv("QDRANT_API_KEY")
    qdrant_url = os.getenv("QDRANT_API_URL")
    qclient = QdrantClient(
        url=qdrant_url,
        api_key=qdrant_api_key,
        timeout=60,
    )

    answers = search_answers(
        question=question,
        language=language,
        qclient=qclient,
        openai_client=client,
        embeddings_model=model,
        collection=collection_name,
    )

    assert len(answers) > 0
