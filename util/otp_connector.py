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


def get_filtered_articles(path, sources, source_types=None, regions=None, dates=None, kw_ne=None, n=2000):
    # TODO: split archive df into two indexes: art_ind+text, art_ind+other
    # example of format: dates = (datetime.date(2022, 1, 1), datetime.date(2022, 1, 27))
    if kw_ne is None:
        kw_ne = []
    if dates is None:
        dates = []
    if regions is None:
        regions = []
    elif "Федеральные СМИ" in regions:
        regions.extend(["", "Россия"])
    if source_types is None:
        source_types = []
    elif "СМИ" in source_types:
        source_types.extend(["Региональные СМИ", "Федеральные СМИ"])
    query_text = '| readFile format=parquet path=%s' % path
    if len(kw_ne) > 0:
        query_text += '|eval kw_ne_temp = kw_ne | makemv delim=";" kw_ne_temp | mvexpand kw_ne_temp'
        query_text += "| where " + " OR ".join([f'like(kw_ne_temp, "%{kw}%")' for kw in kw_ne])
        query_text += "| dedup art_ind"
    if len(sources) > 0:
        source_condition = " OR ".join([f'source="{source}"' for source in sources])
    else:
        source_condition = ""
    if len(source_types) > 0:
        source_type_condition = " OR ".join([f'source_type="{source}"' for source in source_types])
    else:
        source_type_condition = ""
    if len(source_condition + source_type_condition) > 0:
        if len(sources) > 0 and len(source_types) > 0:
            query_text += "| where " + source_condition + " OR " + source_type_condition
        else:
            query_text += "| where " + source_condition + source_type_condition
    if len(regions) > 0:
        query_text += "| where " + " OR ".join([f'region="{reg}"' for reg in regions])
    if len(dates) > 0:
        start, end = dates
        start = time.mktime(start.timetuple())
        end = time.mktime(end.timetuple())
        query_text += "| where _time>=%d AND _time<=%d" % (start, end)
    query_text += "| dedup art_ind | sort -_time | head %d" % n
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
