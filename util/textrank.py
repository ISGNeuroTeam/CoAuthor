from collections import OrderedDict

import numpy as np


def get_vocab(text):
    """Get all tokens"""
    vocab = OrderedDict()
    i = 0
    for word in text:
        if word not in vocab:
            vocab[word] = i
            i += 1
    return vocab


def get_token_pairs(window_size, text):
    """Build token_pairs from windows in sentences"""
    token_pairs = list()
    for i, word in enumerate(text):
        for j in range(i + 1, i + window_size):
            if j >= len(text):
                break
            pair = (word, text[j])
            if pair not in token_pairs:
                token_pairs.append(pair)
    return token_pairs


def symmetrize(a):
    return a + a.T - np.diag(a.diagonal())


def get_matrix(vocab, token_pairs):
    """Get normalized matrix"""
    # Build matrix
    vocab_size = len(vocab)
    g = np.zeros((vocab_size, vocab_size), dtype='float')
    for word1, word2 in token_pairs:
        i, j = vocab[word1], vocab[word2]
        g[i][j] = 1

    # Get Symmetric matrix
    g = symmetrize(g)

    # Normalize matrix by column
    norm = np.sum(g, axis=0)
    g_norm = np.divide(g, norm, where=norm != 0)  # this is ignore the 0 element in norm

    return g_norm


def text_rank(text, kw_num, window_size=4, steps=10, min_diff=1e-5, d=0.85):
    # Build vocabulary
    vocab = get_vocab(text)

    # Get token_pairs from windows
    token_pairs = get_token_pairs(window_size, text)

    # Get normalized matrix
    g = get_matrix(vocab, token_pairs)

    # Initialization for weight(pagerank value)
    pr = np.array([1] * len(vocab))

    # Iteration
    previous_pr = 0
    for epoch in range(steps):
        pr = (1 - d) + d * np.dot(g, pr)
        if abs(previous_pr - sum(pr)) < min_diff:
            break
        else:
            previous_pr = sum(pr)

    # Get weight for each node
    node_weight = dict()
    for word, index in vocab.items():
        node_weight[word] = pr[index]

    predicted_kw = [k[0] for k in sorted(node_weight.items(), key=lambda x: x[1], reverse=True)[:kw_num]]
    return predicted_kw
