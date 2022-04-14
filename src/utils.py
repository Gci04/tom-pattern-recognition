import numpy as np
import pandas as pd
import zipfile

# For data preprocessing
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt

# For matrix profile calculations
import stumpy

def get_data(data_path='../Data/sample_data.zip', target_metric='total_changed'):
    cols_to_select = ['commit_datetime', 'full_name'] + [target_metric]
    zf = zipfile.ZipFile(data_path)
    repository_hist_df = pd.read_csv(zf.open('commits_data.csv'), usecols=cols_to_select, parse_dates=['commit_datetime'], index_col='commit_datetime')

    result = {}
    for name, group in repository_hist_df.groupby('full_name'):
        result[name] = group.sort_index()[target_metric].values.astype(np.float64)
    return result

def search_pattern(T, query_pattern):
    distance_profile = stumpy.match(query_pattern, T)
    return distance_profile

def get_topk_motifs(T, k=5, m=7):
    mp = stumpy.stump(T, m=m)
    top_k_motifs_idx = np.argsort(mp[:, 0])[:k]
    return top_k_motifs_idx, np.array([T[i:i+m] for i in top_k_motifs_idx])

def UnanchoredChain(T, m=7):
    mp = stumpy.stump(T, m=m)
    all_chain_set, unanchored_chain = stumpy.allc(mp[:, 2], mp[:, 3])

def get_pattern(repo, m=7):
    indx, motifs = get_topk_motifs(repo, m=m, k=7)
    return repo, indx, motifs

def consensus_motif(Ts, m):
    return stumpy.ostinato(Ts,m)
