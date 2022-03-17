from natasha import MorphVocab, Doc, NewsNERTagger, NewsMorphTagger, NewsEmbedding, Segmenter, PER, NamesExtractor


def finder(text):
    segmenter = Segmenter()
    morph_vocab = MorphVocab()
    emb = NewsEmbedding()
    ner_tagger = NewsNERTagger(emb)
    morph_tagger = NewsMorphTagger(emb)
    names_extractor = NamesExtractor(morph_vocab)
    doc = Doc(text)
    doc.segment(segmenter)
    doc.sents
    doc.tokens
    doc.tag_morph(morph_tagger)
    doc.tag_ner(ner_tagger)
    ner_types = {'LOC': [], 'ORG': [], 'PER': []}
    per = list()
    for span in doc.spans:
        span.normalize(morph_vocab)
        ner_types[span.type].append(span.normal)
        if span.type == PER:
            span.extract_fact(names_extractor)
    names = {_.normal: _.fact.as_dict for _ in doc.spans if _.fact}
    for value in names.values():
        if 'last' in value:
            per.append(' '.join(list(value.values())[:2]))
    loc = list(set(ner_types['LOC']))
    org = list(set(ner_types['ORG']))
    ner = loc
    ner.extend(org)
    ner.extend(per)
    return ner
