import numpy as np
import torch
from sklearn.metrics.pairwise import cosine_similarity


def sentences_to_embeddings(sentences, tokenizer, model):
    encoded_input = tokenizer(sentences, padding=True, truncation=True, max_length=64, return_tensors='pt')
    with torch.no_grad():
        model_output = model(**encoded_input)
    embeddings = model_output.pooler_output
    embeddings = torch.nn.functional.normalize(embeddings)
    mean_embedding = np.mean(embeddings.numpy(), axis=0)
    return mean_embedding


# def embed_labse(text, tokenizer, model):
#     # , model_path, tokenizer_path
#     encoded_input = tokenizer(text, padding=True, truncation=True, max_length=64, return_tensors='pt')
#     with torch.no_grad():
#         model_output = model(**encoded_input)
#     embeddings = model_output.pooler_output
#     embeddings = torch.nn.functional.normalize(embeddings)
#     return embeddings[0].cpu().numpy()


def find_sim_texts(texts, input_vec, ref_number, full_output=False):
    archive_vecs = np.array([x.split("; ") for x in texts["embedding"].values])
    similarity_matrix = cosine_similarity(input_vec.reshape(1, -1), archive_vecs)
    sim_texts = list(zip(texts["art_ind"], similarity_matrix[0]))
    if len(sim_texts) > ref_number and not full_output:
        sim_texts = sorted(sim_texts, key=lambda x: x[1], reverse=True)[:ref_number]
    return sim_texts
