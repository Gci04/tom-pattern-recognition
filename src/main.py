from utils import *
import numpy as np

all_data = get_data()
del all_data['xavzelada/repo_test']
issues_df = read_issues()

def approach1(Ts, m, threshold_dist=0.01, save_plots=False):
    '''Maximize the number of matches of Q. For each repo time series find a
    pattern and then match with all other repositories time series'''
    result = {}
    N = len(Ts)
    for i in range(N):
        _ , q = get_topk_motifs(Ts[i], k=5, m=m)
        count = 0
        for j in range(N):
            if i == j: continue
            distance_profile = search_pattern(Ts[j], q[0], max_distance=threshold_dist)
            count += len(distance_profile)

        result[i] = count
    if min(result.values()) > 0: print(result)
    selected_t = Ts[max(result, key=result.get)]
    mp = stumpy.stump(selected_t, m=m)
    top_k_motifs_idx = np.argsort(mp[:, 0])[:10]

    if save_plots :
        plot_patterns(selected_t, mp, top_k_motifs_idx, m, save=save_plots)

def approach2(Ts, m):
    '''Join all the repositories and find a pattern'''
    joinedTs = np.concatenate(Ts)
    print(joinedTs.shape)
    _, q = get_topk_motifs(joinedTs, k=1, m=m)
    print(q)

def approach3(Ts, m):
    '''Find the z-normalized consensus pattern of multiple time series'''
    central_radius, central_Ts_idx, central_subseq_idx = consensus_motif(Ts, m)
    consensus_pattern = Ts[central_Ts_idx][central_subseq_idx:central_subseq_idx+m]

    result = {}
    tot_found = 0
    overall_distance = 0.0
    min_found = np.inf
    min_indx = central_Ts_idx

    print(f'Consensus pattern : {*consensus_pattern,}')
    print(f'Central radius : {central_radius}')

    for i in range(len(Ts)):
        distance_profile = search_pattern(Ts[i], consensus_pattern)
        result[i] = distance_profile[:,1]
        if central_Ts_idx == i : continue
        tot_found += len(distance_profile)
        if len(distance_profile) == 0:
            min_indx = 0
            continue
        overall_distance += distance_profile[:,0].sum()
        if len(distance_profile) < min_found:
            min_found = len(distance_profile)
            min_indx = i

    print(f'Total Distance : {overall_distance}')
    print(f'Total Found patterns : {tot_found}')
    print(f'Min Found patterns : {min_found}, indx: {min_indx}')

    return central_Ts_idx, central_subseq_idx, result

def print_repos_stats():
    global all_data
    for k, v in all_data.items():
        print(f'{k} : {len(v.get("time_stamps"))} commits')

if __name__ == '__main__':
    Ts = []
    projects_names_map = {}

    for i, (k, v) in enumerate(all_data.items()):
        Ts.append(v.get('total_changed'))
        projects_names_map[i] = k

    print(projects_names_map)
    print_repos_stats()
    m = 14
    repo_idx, seq_idx, all_patterns = approach3(Ts, m)
    print(projects_names_map[repo_idx])
    print(all_data[projects_names_map[repo_idx]].get('time_stamps')[seq_idx:seq_idx+m])

    for k, v in all_patterns.items():
        print(projects_names_map[k])
        print(all_data[projects_names_map[k]].get('time_stamps')[v[0]:v[0]+m])

    # for m in [5, 7, 14, 21, 30, 40, 50]:
    #     for d in [0.001, 0.01, 0.1, 1.0, 2.0, 3.0]:
    #         print(f'({m}, {d})')
    #         approach1(Ts,  m=m, threshold_dist=d)
