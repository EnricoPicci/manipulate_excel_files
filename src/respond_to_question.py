import os
from litellm import completion
from openai import OpenAI
from qdrant_client import QdrantClient

from src.query_data import search_answers


def summarize_response(
    answers_records,
    prompt=None,
    model="gpt-4o",
    verbose=False,
):
    if prompt is None:
        prompt = """You are a sales specialist at a Software Company that develops and sells a platform for the Insurance Industry.
You are in charge of answering to a question in an Request For Proposal (RFP) about the platform.
You have a long hitory of answers to similar questions.
Please summarize an answer using the following answers retrieved for similar questions and do not add anything else but the answer:"""

    answers = [record["answer"] for record in answers_records]
    answers_text = "\n\n".join([f"- {answer}" for answer in answers])

    messages = [
        {
            "content": f"""{prompt}

Previous answers: 
{answers_text}.

""",
            "role": "user",
        }
    ]

    if verbose:
        print(f"message content:")
        print(f"Query: {messages[0]['content']}")

    result = completion(
        model=model, temperature=0, messages=messages, request_timeout=120
    )
    result = result["choices"][0]["message"]["content"]

    return result


def build_response(
    question,
    language,
    prompt=None,
    embeddings_model="text-embedding-3-small",
    n_answers=5,
    verbose=False,
):
    collection_name = "r_r_questions_1"

    openai_client = OpenAI()
    embeddings_model = "text-embedding-3-small"

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
        embeddings_model=embeddings_model,
        collection=collection_name,
        n_answers=n_answers,
        verbose=verbose,
    )

    new_response = summarize_response(
        answers_records=answers, prompt=prompt, verbose=verbose
    )

    answers_single_record = {}

    # add the original question and the new response to the record
    answers_single_record["question"] = question
    answers_single_record["response"] = new_response

    # answers is a list of dictionaries with keys: question, answer, domain, date, file
    # we need to create a new record which contains a series of fields like these
    # pre_q_1, pre_a_1, pre_domain_1, pre_date_1, pre_file_1, pre_q_2, pre_a_2, pre_domain_2, pre_date_2, pre_file_2, ...
    for i, answer in enumerate(answers):
        answers_single_record[f"pre_q_{i}"] = answer["question"]
        answers_single_record[f"pre_a_{i}"] = answer["answer"]
        answers_single_record[f"pre_domain_{i}"] = answer["domain"]
        answers_single_record[f"pre_date_{i}"] = answer["date"]
        answers_single_record[f"pre_file_{i}"] = answer["file"]

    return answers_single_record
