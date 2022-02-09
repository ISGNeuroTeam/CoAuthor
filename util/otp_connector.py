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


def get_filtered_articles(path, dates, sources):  # kw_ne
    # dates = (datetime.date(2022, 1, 1), datetime.date(2022, 1, 27))
    query_text = '| readFile format=parquet path=%s' % path
    # |eval kw_ne_temp = kw_ne | makemv delim=";" kw_ne_temp | mvexpand kw_ne_temp
    # if len(kw_ne) > 0:
    #     query_text += "| where " + " OR ".join([f'kw_ne="{kw}"' for kw in kw_ne])
    if len(sources) > 0:
        query_text += "| where " + " OR ".join([f'source="{source}"' for source in sources])
    if len(dates) > 0:
        start, end = dates
        start = time.mktime(start.timetuple())
        end = time.mktime(end.timetuple())
        query_text += "| where _time>=%d AND _time<=%d" % (start, end)
    query_text += "|sort -_time | head 2000"
    job = conn.jobs.create(query_text=query_text, cache_ttl=cache_ttl, tws=tws, twf=twf, blocking=True)
    return pd.DataFrame(job.dataset.load())


def get_unique_source_topics(path, feature):
    query_text = "| readFile format=parquet path=%s | chart count by %s " % (path, feature)
    job = conn.jobs.create(query_text=query_text, cache_ttl=cache_ttl, tws=tws, twf=twf, blocking=True)
    result = pd.DataFrame(job.dataset.load())
    return result


def get_text_features_eep(text):
    query_text = '| makeresults | eval text="%s" | runProcess script=kw_textrank_eep.kw_extraction ' \
                 '| runProcess script=doc_embedding.worker' % text  # | writeFile format=parquet path=%s
    job = conn.jobs.create(query_text=query_text, cache_ttl=cache_ttl, tws=tws, twf=twf, blocking=True)
    return pd.DataFrame(job.dataset.load())