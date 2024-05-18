import os
from openai import OpenAI
from qdrant_client import QdrantClient

from src.read_excels import records_from_excel_files
from src.read_rfx_historical_data import records_from_rfx_historical_data
from src.upload_rfx_historical_data_to_qdrant import upload_rfx_questions


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
question_records = records_from_rfx_historical_data(records, languages)
question_records = question_records[:5]

upload_rfx_questions(
    question_records, collection_name, client, qclient, model, verbose=True
)
