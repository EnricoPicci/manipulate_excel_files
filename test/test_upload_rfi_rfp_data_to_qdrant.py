import os
from openai import OpenAI
from qdrant_client import QdrantClient

from src.read_data import records_from_excel_files
from src.read_rfi_rfp_data import records_from_rfi_rfp
from src.upload_rfi_rfp_data_to_qdrant import upload_rfi_rfp_questions


def test_upload_rfi_rfp_questions():
    folder_path = "test_data/excel_files"
    languages = ["en", "it", "fr", "de", "es"]

    collection_name = "r_r_questions"

    client = OpenAI()
    model = "text-embedding-3-small"

    qdrant_api_key = os.getenv("QDRANT_API_KEY")
    qdrant_url = os.getenv("QDRANT_API_URL")
    qclient = QdrantClient(
        url=qdrant_url,
        api_key=qdrant_api_key,
        timeout=60,
    )

    records = records_from_excel_files(folder_path)
    question_records = records_from_rfi_rfp(records, languages)

    upload_rfi_rfp_questions(question_records, collection_name, client, qclient, model)

    # Check if the collection is created
    collections = qclient.collections.list()
    collection_names = [collection.name for collection in collections.collections]
    assert collection_name in collection_names
