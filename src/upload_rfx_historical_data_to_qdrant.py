import uuid
from openai import OpenAI
from qdrant_client import QdrantClient, models

from src.encoding import encode_sentence
from test.embedding_models import get_embedding_model_vec_size


def generate_point_from_rfx_question(
    question,
    answer,
    language,
    domain,
    date,
    file,
    client,
    embedding_model,
    verbose=False,
):
    if verbose:
        print(f">>>>>>>>>>>>>>>> Processing question {question}")
    embedding = encode_sentence(question, client, embedding_model)
    payload = {
        "question": question,
        "answer": answer,
        "language": language,
        "domain": domain,
        "date": date,
        "file": file,
    }
    point = models.PointStruct(
        id=generate_uuid(),
        vector=embedding,
        payload=payload,
    )
    return point


def generate_uuid():
    uuid_val = uuid.uuid4()
    return "{}-{}-{}-{}-{}".format(
        uuid_val.hex[:8],
        uuid_val.hex[8:12],
        uuid_val.hex[12:16],
        uuid_val.hex[16:20],
        uuid_val.hex[20:],
    )


def upload_points(points, collection_name, qclient, vec_size, verbose=False):
    # if the client is not a QdrantClient object, raise an error
    if not isinstance(qclient, QdrantClient):
        raise ValueError("qclient must be a QdrantClient object")
    existing_collections = qclient.get_collections()
    # exixting_collection_names is a list of the names of the existing collections
    existing_collection_names = [
        collection.name for collection in existing_collections.collections
    ]
    if collection_name not in existing_collection_names:
        qclient.create_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(
                size=vec_size,
                distance=models.Distance.COSINE,
            ),
        )
    # split points into blocks points and then upload them one block at a time
    if verbose:
        print(f"Uploading {len(points)} points to collection {collection_name}")
    block_size = 10
    for i in range(0, len(points), block_size):
        if verbose:
            print(f"Uploading points {i} to {i+block_size}")
        qclient.upsert(
            collection_name=collection_name, points=points[i : i + block_size]
        )


def upload_rfx_questions(
    question_records,
    collection_name,
    openai_client,
    qclient,
    embedding_model,
    verbose=False,
):
    points = []
    num_questions = len(question_records)
    for i, question_rec in enumerate(question_records):
        if verbose:
            print(
                f"Generating embeddings for question {question_rec['Question']} - {i} of {num_questions}"
            )
        # read the relevant fields from the question record
        question = question_rec["Question"]
        answer = question_rec["Answer"]
        language = question_rec["Language"]
        domain = question_rec["Domain"]
        date = question_rec["Date"]
        file = question_rec["File_Path"]

        point = generate_point_from_rfx_question(
            question,
            answer,
            language,
            domain,
            date,
            file,
            openai_client,
            embedding_model,
            verbose,
        )
        points.append(point)

    vec_size = get_embedding_model_vec_size(embedding_model)
    upload_points(points, collection_name, qclient, vec_size, verbose)
