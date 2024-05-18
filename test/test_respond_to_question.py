import os
from openai import OpenAI
from qdrant_client import QdrantClient

from src.respond_to_question import (
    build_response_multi_records,
    build_response_one_record,
    summarize_response,
)
from src.query_data import search_answers


def test_summarize_response():
    question = "Do you comply with GDPR and other local EU Data Protection regulations?"
    language = "en"

    collection_name = "r_r_questions_1"

    openai_client = OpenAI()
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
        openai_client=openai_client,
        embeddings_model=model,
        collection=collection_name,
    )

    new_response = summarize_response(answers_records=answers, verbose=True)

    assert len(new_response) > 0


def build_response_one_record():
    question = "Do you comply with GDPR and other local EU Data Protection regulations?"
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

    response_record = build_response_one_record(
        question=question,
        language=language,
        qclient=qclient,
        collection_name=collection_name,
        embeddings_model=embeddings_model,
        openai_client=openai_client,
        verbose=True,
    )

    assert len(response_record) > 0


def test_build_response_multi_records():
    question = "Do you comply with GDPR and other local EU Data Protection regulations?"
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

    response_records = build_response_multi_records(
        question=question,
        language=language,
        qclient=qclient,
        collection_name=collection_name,
        embeddings_model=embeddings_model,
        openai_client=openai_client,
        verbose=True,
    )

    assert len(response_records) > 0
