from litellm import completion


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
Please summarize an answer using the following answers retrieved for similar questions:"""

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
