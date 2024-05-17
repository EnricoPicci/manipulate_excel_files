# define the list of possible models to use for embedding with OpenAI
EMBEDDINGS_MODELS = [
    {"name": "text-embedding-3-small", "vec_size": 1536},
    {"name": "text-embedding-3-large", "vec_size": 3072},
    {"name": "text-embedding-ada-002", "vec_size": 1536},
]


def get_embedding_model_names():
    return [model["name"] for model in EMBEDDINGS_MODELS]


def get_embedding_model_vec_size(name):
    for model in EMBEDDINGS_MODELS:
        if model["name"] == name:
            return model["vec_size"]
    # throw an error if the model name is not found
    raise ValueError(
        f"Invalid model: {name}. Must be one of {get_embedding_model_names()}"
    )
