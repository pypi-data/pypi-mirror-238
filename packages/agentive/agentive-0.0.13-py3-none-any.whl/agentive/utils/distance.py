import numpy as np


def cosine_similarity(query, documents):
    # Ensure both query_embedding and document_embedding are NumPy arrays
    query_embedding = np.array(query)
    document_embedding = np.array(documents)

    # Calculate the dot product
    dot_product = np.dot(document_embedding, query_embedding.T)

    # Calculate the norms
    query_norm = np.linalg.norm(query_embedding)
    document_norms = np.linalg.norm(document_embedding)

    # Calculate the cosine similarities
    cosine_similarities = dot_product / (query_norm * document_norms)

    return cosine_similarities
