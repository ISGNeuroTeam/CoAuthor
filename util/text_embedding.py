import numpy as np
import torch
from sklearn.metrics.pairwise import cosine_similarity
from transformers import AutoTokenizer, AutoModel


def embed_bert_cls(text, model_path, tokenizer_path):
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModel.from_pretrained(tokenizer_path)
    # TODO: add file not found error

    t = tokenizer(text, padding=True, truncation=True, return_tensors='pt')
    with torch.no_grad():
        model_output = model(**{k: v.to(model.device) for k, v in t.items()})
    embeddings = model_output.last_hidden_state[:, 0, :]
    embeddings = torch.nn.functional.normalize(embeddings)
    return embeddings[0].cpu().numpy()


def find_sim_texts(texts, input_vec, ref_number, similarity_threshold, full_output=False):
    archive_vecs = np.array([x.tolist() for x in texts["bert_vec"].values])
    similarity_matrix = cosine_similarity(input_vec.reshape(1, -1), archive_vecs)
    sim_texts = list(filter(lambda x: x[1] > similarity_threshold,
                            list(zip(texts["art_ind"], similarity_matrix[0]))))
    if len(sim_texts) > ref_number and not full_output:
        sim_texts = sorted(sim_texts, key=lambda x: x[1], reverse=True)[:ref_number]
    return sim_texts
