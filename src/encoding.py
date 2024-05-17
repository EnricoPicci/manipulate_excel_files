from openai import OpenAI


def encode_sentence(text, client, embeddings_model="text-embedding-3-small"):
    # client must be an instance of OpenAI class, if not create one
    if not isinstance(client, OpenAI):
        client = OpenAI()
    text = text.replace("\n", " ")
    return (
        client.embeddings.create(input=[text], model=embeddings_model).data[0].embedding
    )
