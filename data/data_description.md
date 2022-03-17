# Data Description
Input file must be provided in parquet format. If you have csv data, you can save it as parquet using pandas function [pandas.DataFrame.to_parquet](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_parquet.html).  

## Columns
* art_ind - index of the article in format "[date]: [title]"
* url - link to the original article
* title - raw newspaper title
* text - raw newspaper text
* date - publish date in format DD.MM.YYYY
* _time - publish date in UNIX format
* source - source of the newspaper (e.g. "Lenta.ru")
* kw_ne - list of keywords and named entities from newspaper text, lemmatized
* clean_text - preprocessed text, tokens inside one sentence separated with one space, sentences separated with "###SENT###" (see example)
* bert_vec - document embedding

## Methods
* Document embedding can be produced with [rubert-tiny](https://huggingface.co/cointegrated/rubert-tiny).
* Text preprocessing includes lemmatization, stop words removing, punctuation and digits removing and can be done with [text_util/data_preprocessing.py](../text_util/data_preprocessing.py).