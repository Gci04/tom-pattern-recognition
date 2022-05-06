import numpy as np
import pandas as pd
import zipfile, re, json
import matplotlib.pyplot as plt

# For data preprocessing
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt

# For matrix profile calculations
import stumpy

def get_data(data_path='../Data/tom_sample_data.zip', target_file='tom_commits_metrics.csv', target_metric='total_changed'):
    cols_to_select = ['commit_datetime', 'full_name'] + [target_metric]
    zf = zipfile.ZipFile(data_path)
    repository_hist_df = pd.read_csv(zf.open(target_file), usecols=cols_to_select, parse_dates=['commit_datetime'], index_col='commit_datetime')

    result = {}
    max_commits = 0
    for name, group in repository_hist_df.groupby('full_name'):
        group.sort_index(inplace=True)
        a = group.index[-1] - group.index[0]
        if a.days > 365 or group.shape[0] < 50: continue
        if group.shape[0] > max_commits:
            max_commits = group.shape[0]
        temp = {}
        temp[target_metric] = group[target_metric].values.astype(np.float64)
        temp['time_stamps'] = group.index
        result[name] = temp
    print(f'total filtered repos : {len(result)}')
    print(f'Max commits : {max_commits}')
    return result

def read_issues(data_path='../Data/tom_sample_data.zip'):
    json_data = None
    data = None
    with zipfile.ZipFile(data_path, 'r') as z:
        with z.open('tom_issues_info.json') as f:
            data = f.read()
            json_data = json.loads(data)

    issues_df = pd.json_normalize(json_data['tom_issues_infos'])
    cols_to_select = ['repo_fullname','title','state','created_at_ext','updated_at_ext','closed_at_ext','comments_count','body_length']
    issues_df = issues_df[cols_to_select]
    for col in ['created_at_ext', 'updated_at_ext', 'closed_at_ext']:
        issues_df[col] = pd.to_datetime(pd.to_datetime(issues_df[col]).dt.strftime('%Y-%m-%d %H:%M:%S'))
    return issues_df

def data_distribution(data_path='../Data/tom_sample_data.zip', target_file='tom_commits_metrics.csv', target_metric='total_changed'):
    cols_to_select = ['commit_datetime', 'full_name'] + [target_metric]
    zf = zipfile.ZipFile(data_path)
    repository_hist_df = pd.read_csv(zf.open(target_file), usecols=cols_to_select, parse_dates=['commit_datetime'], index_col='commit_datetime')

    result = []
    for name, group in repository_hist_df.groupby('full_name'):
        group.sort_index(inplace=True)
        repo_age = group.index[-1] - group.index[0]
        repo_tot_commits = len(group)
        result.append([int(repo_age.days/30), repo_tot_commits])

    result_df = pd.DataFrame(result, columns=['age', 'commits'])
    hist = result_df.hist()
    plt.show()

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
