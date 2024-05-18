from qdrant_client import models
from src.upload_rfx_data_to_qdrant import encode_sentence


def search_answers(
    question,
    language,
    qclient,
    openai_client,
    embeddings_model,
    collection,
    n_answers=5,
    verbose=False,
):
    if verbose:
        print(f">>>>>>>>>>>>>>>> Searching for answers to question {question}")
        print(f">>>>>>>>>>>>>>>> Language: {language}")
        print(f">>>>>>>>>>>>>>>> Collection: {collection}")

    hits = qclient.search(
        collection_name=collection,
        query_vector=encode_sentence(question, openai_client, embeddings_model),
        with_payload=True,  # Set to True to include payload in the search results
        limit=n_answers,
        query_filter=models.Filter(
            must=[
                models.FieldCondition(
                    key="language",
                    match=models.MatchValue(
                        value=language,
                    ),
                )
            ]
        ),
    )

    enriched_answers = []
    for hit in hits:
        enriched_answers.append(
            {
                "question": hit.payload["question"],
                "answer": hit.payload["answer"],
                "domain": hit.payload["domain"],
                "date": hit.payload["date"],
                "file": hit.payload["file"],
                "id": hit.id,
            }
        )

    if verbose:
        print(f">>>>>>>>>>>>>>>> Found {len(enriched_answers)} answers")
        for i, answer in enumerate(enriched_answers):
            print(f">>>>>>>>>>>>>>>> Answer {i+1}: {answer}")

    return enriched_answers


def build_answer_records(answers):
    answer_records = []
    for answer in answers:
        answer_records.append(
            {
                "question": answer["question"],
                "answer": answer["answer"],
                "domain": answer["domain"],
                "date": answer["date"],
                "file": answer["file"],
            }
        )
    return answer_records
