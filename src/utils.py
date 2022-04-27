import numpy as np
import pandas as pd
import zipfile, re

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
        group.sort_index(inplace=True)
        temp = {}
        temp[target_metric] = group[target_metric].values.astype(np.float64)
        temp['time_stamps'] = group.index
        result[name] = temp
    return result
def read_issues():
    res = []
    COMMA_MATCHER = re.compile(r",(?=(?:[^\"']*[\"'][^\"']*[\"'])*[^\"']*$)")
    with zipfile.ZipFile('../Data/sample_data.zip') as z:
        with z.open('issues_data.csv') as f:
            for line in f.readlines():
                line = line.decode("utf-8").strip()
                split_result = COMMA_MATCHER.split(line)
                if len(split_result) != 21:
                    tokens = line.split(',')
                    if len(tokens) == 21:
                        res.append(tokens)
                else:
                    res.append(split_result)

    df = pd.DataFrame(res[1:],columns=res[0])
    return df

def search_pattern(T, query_pattern, max_distance=1.0):
    distance_profile = stumpy.match(query_pattern, T, max_distance=max_distance)
    return distance_profile

def get_topk_motifs(T, k=5, m=7):
    mp = stumpy.stump(T, m=m)
    top_k_motifs_idx = np.argsort(mp[:, 0])[:k]
    return top_k_motifs_idx, np.array([T[i:i+m] for i in top_k_motifs_idx])

def get_topk_distict_motifs(T, m=7, min_neighbors=5):
    '''A subsequence, Q, becomes a candidate motif if there are at least min_neighbor number
    of other subsequence matches in T (outside the exclusion zone) with a distance less
    or equal to max_distance.'''

    mp = stumpy.stump(T, m=m)
    motif_distances, motif_indices = stumpy.motifs(T, mp[:, 0], min_neighbors=min_neighbors)
    return motif_distances, motif_indices

def UnanchoredChain(T, m=7):
    mp = stumpy.stump(T, m=m)
    all_chain_set, unanchored_chain = stumpy.allc(mp[:, 2], mp[:, 3])

def get_pattern(repo, m=7):
    indx, motifs = get_topk_motifs(repo, m=m, k=7)
    return repo, indx, motifs

def consensus_motif(Ts, m):
    return stumpy.ostinato(Ts, m)

def plot_patterns(T, mp, patterns_index, m, save=False):
    fig, axs = plt.subplots(2,1,sharex=True, figsize=(10,7), gridspec_kw={'hspace': 0})
    axs[0].set_ylabel('T', fontsize='20')
    axs[0].plot(T)
    axs[1].plot(mp[:,0],c='green', linewidth=2)
    axs[1].set_ylabel('P1', fontsize='20')

    for idx in patterns_index:
      axs[0].plot(np.arange(idx, idx+m), T[idx:idx+m], c='red', linewidth=2)
      axs[0].axvline(x=idx, linestyle='dashed', c='black')

    if save :
        plt.savefig(f'All_data_{m}.eps')
