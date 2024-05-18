from src.read_rfx_questions import read_rfx_questions
from src.respond_to_question import build_response_multi_records


def response_records_for_rfx(
    rfx_questions_excel,
    language,
    qclient,
    collection_name,
    openai_client,
    embeddings_model="text-embedding-3-small",
    prompt=None,
    n_answers=5,
    verbose=False,
):
    questions = read_rfx_questions(rfx_questions_excel)

    response_records = []
    rec_count = 0
    for question in questions:
        response = build_response_multi_records(
            question=question,
            language=language,
            qclient=qclient,
            collection_name=collection_name,
            openai_client=openai_client,
            embeddings_model=embeddings_model,
            prompt=prompt,
            n_answers=n_answers,
            verbose=verbose,
        )
        for rec in response:
            rec_count += 1
            rec["num"] = rec_count
        response_records.extend(response)

    return response_records


def write_response_records_to_excel(response_records, output_excel):
    import pandas as pd

    df = pd.DataFrame(response_records)
    df.to_excel(output_excel, index=False)


def respond_to_rfx(
    rfx_questions_excel,
    language,
    output_excel,
    qclient,
    collection_name,
    openai_client,
    embeddings_model="text-embedding-3-small",
    prompt=None,
    n_answers=5,
    verbose=False,
):
    response_records = response_records_for_rfx(
        rfx_questions_excel=rfx_questions_excel,
        language=language,
        qclient=qclient,
        collection_name=collection_name,
        openai_client=openai_client,
        embeddings_model=embeddings_model,
        prompt=prompt,
        n_answers=n_answers,
        verbose=verbose,
    )
    write_response_records_to_excel(response_records, output_excel)

    print(f"Response records written to {output_excel}")
