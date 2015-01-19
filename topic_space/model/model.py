"""Visualizations of the material science research files"""

import json
import os
import random

import numpy as np
import pandas as pd
import pattern.vector as pv

import bokeh.plotting as plt



DATA_FILE = "msr-data.json"
STOPWORD_FILE = "stopwords_wordnet.txt"


def create_models(group):
    docs = [pv.Document(item, threshold=1) for item in group]
    return pv.Model(docs, weight=pv.TFIDF)


def get_models_by_year(df):
    return df[['year', 'abstract']].groupby('year').apply(create_models)


def get_clusters_by_year(df, k=5):
    return get_models_by_year(df).apply(lambda x: x.cluster(pv.KMEANS, k=k))


def lsa_apply(df):
    m = pv.Model([pv.Document(a) for a in df['abstract']], weight=pv.TFIDF)
    return m.reduce(2)


def get_lsa_by_year(df):
    return df[['year', 'abstract']].groupby('year').apply(lsa_apply)



def interesting_words(lsa, n=3):
    lsa_df = pd.DataFrame.from_dict(lsa.concepts)
    res = []
    for row, series in lsa_df.iterrows():
        series.sort(ascending=False)
        print series[0]
        if series[0] <= 1e-8:
            print "in pass"
            continue
    res_df = pd.DataFrame(res).transpose()
    res_df.fillna(0, inplace=True)
    return res_df


def interesting_words_1(lsa, n=3):
    lsa_df = pd.DataFrame.from_dict(lsa.concepts)
    res = []
    for row, series in lsa_df.iterrows():
        s = sorted([(abs(y), x) for x, y in series.iterkv()], reverse=True)
        res.extend([x for y,x in s[:n]])
    return set(res)



if __name__ == "__main__":
    #main_example()
    pass
