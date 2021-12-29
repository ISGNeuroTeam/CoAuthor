from razdel import sentenize
from sumy.nlp.tokenizers import Tokenizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.summarizers.lex_rank import LexRankSummarizer


def lexrank_sum(texts_set, sent_num=1):
    summarizer = LexRankSummarizer()
    summary = []
    for clean_text, text in texts_set:
        temp_text = clean_text.replace("###SENT###", " .\n")
        doc_dict = dict(zip(clean_text.split("###SENT###"), sentenize(text)))
        my_parser = PlaintextParser.from_string(temp_text, Tokenizer('russian'))
        doc_sum = summarizer(my_parser.document, sentences_count=sent_num)
        doc_keys = [sent._text.replace(".", "").strip() for sent in doc_sum]
        doc_raw_sum = [doc_dict[key].text for key in doc_keys if key in doc_dict]
        summary.append(doc_raw_sum)
    return summary
