import time

import pandas as pd
from envyaml import EnvYAML
from ot_simple_connector.connector import Connector

config = EnvYAML("config_local.yaml")

host = config["connection"]["host"]
port = config["connection"]["port"]
user = config["connection"]["user"]
password = config["connection"]["password"]
loglevel = config["connection"]["loglevel"]

conn = Connector(host, port, user, password, loglevel=loglevel)
cache_ttl = 59
tws = 11
twf = 22


def get_dedup_articles(path):
    query_text = "| readFile format=parquet path=%s | dedup art_ind | head 100" % path
    job = conn.jobs.create(query_text=query_text, cache_ttl=cache_ttl, tws=tws, twf=twf, blocking=True)
    return pd.DataFrame(job.dataset.load())


def get_keywords(text):
    filename = str(time.time()) + "###" + text[:10].replace(" ", "_")
    query_text = '| makeresults | eval text="%s" | runProcess script=kw_textrank_eep.kw_extraction ' \
                 '| writeFile format=parquet path=%s ' % (text, filename)
    job = conn.jobs.create(query_text=query_text, cache_ttl=cache_ttl, tws=tws, twf=twf, blocking=True)
    return pd.DataFrame(job.dataset.load()), filename


def get_embedding(filename):
    new_filename = str(time.time()) + "###" + filename.split("###")[-1]
    query_text = "| readFile format=parquet path=%s | runProcess script=doc_embedding.worker" \
                 "| writeFile format=parquet path=%s " % (filename, new_filename)
    job = conn.jobs.create(query_text=query_text, cache_ttl=cache_ttl, tws=tws, twf=twf, blocking=True)
    return pd.DataFrame(job.dataset.load()), new_filename


def sim_score(filename, archive_path):
    query_text = '| readFile format = parquet path = %s | eval art_ind = "%s" | makemv embedding delim = "; "' \
                 '| fields art_ind, text, embedding' \
                 '| append [ | readFile format = parquet path = %s ' \
                 '| rename bert_vec_labse as embedding | fields art_ind, text, embedding] | head 10' % (
                     filename, filename, archive_path)
    job = conn.jobs.create(query_text=query_text, cache_ttl=cache_ttl, tws=tws, twf=twf, blocking=True)
    return pd.DataFrame(job.dataset.load())
