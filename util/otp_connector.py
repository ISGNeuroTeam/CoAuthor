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


def get_filtered_articles(path, sources, dates=None, kw_ne=None, n=2000):
    # TODO: split archive df into two indexes: art_ind+text, art_ind+other
    # dates = (datetime.date(2022, 1, 1), datetime.date(2022, 1, 27))
    if kw_ne is None:
        kw_ne = []
    if dates is None:
        dates = []
    query_text = '| readFile format=parquet path=%s' % path
    if len(kw_ne) > 0:
        query_text += '|eval kw_ne_temp = kw_ne | makemv delim=";" kw_ne_temp | mvexpand kw_ne_temp'
        query_text += "| where " + " OR ".join([f'like(kw_ne_temp, "%{kw}%")' for kw in kw_ne])
        query_text += "| dedup art_ind"
    if len(sources) > 0:
        query_text += "| where " + " OR ".join([f'source="{source}"' for source in sources])
    if len(dates) > 0:
        start, end = dates
        start = time.mktime(start.timetuple())
        end = time.mktime(end.timetuple())
        query_text += "| where _time>=%d AND _time<=%d" % (start, end)
    query_text += "|sort -_time | head %d" % n
    job = conn.jobs.create(query_text=query_text, cache_ttl=cache_ttl, tws=tws, twf=twf, blocking=True)
    return pd.DataFrame(job.dataset.load())


def get_unique_values(path, feature):
    query_text = "| readFile format=parquet path=%s " % path
    if feature == "kw_ne":
        query_text += '| makemv delim=";" kw_ne | mvexpand kw_ne'
    query_text += "| chart count by %s " % feature
    job = conn.jobs.create(query_text=query_text, cache_ttl=cache_ttl, tws=tws, twf=twf, blocking=True)
    result = pd.DataFrame(job.dataset.load())
    return result


def get_text_features_eep(text):
    query_text = '| makeresults | eval text="%s" | runProcess script=kw_textrank_eep.kw_extraction ' \
                 '| runProcess script=doc_embedding.worker' % text  # | writeFile format=parquet path=%s
    job = conn.jobs.create(query_text=query_text, cache_ttl=cache_ttl, tws=tws, twf=twf, blocking=True)
    return pd.DataFrame(job.dataset.load())
