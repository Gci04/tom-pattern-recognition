from utils import *
import numpy as np

all_data = get_data()
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
        try:
            result[i] = distance_profile[:,1]
        except Exception as e:
            print(distance_profile)

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
    # all_data
    Ts = []
    projects_names_map = {}
    # data_distribution()

    for i, (k, v) in enumerate(all_data.items()):
        Ts.append(v.get('total_changed'))
        projects_names_map[i] = k

    # print_repos_stats()
    m = 9
    # for m in [5,7,10,14,21]
    repo_idx, seq_idx, all_patterns = approach3(Ts, m)

    d = {}
    all_found = {}
    for k, v in all_patterns.items():
        repo_name = projects_names_map[k]
        temp = []
        temp2 = []
        print(f'\n{repo_name} patterns (anomalies)')
        for idx in v[:]:
            repo_timestamps = all_data[repo_name].get('time_stamps')
            first_commit = min(repo_timestamps)
            mask = np.where(first_commit.replace(year = first_commit.year + 1) > repo_timestamps)[0]
            upper_bound = max(repo_timestamps[mask])

            start = repo_timestamps[idx]
            try:
                end = repo_timestamps[idx+m]
            except Exception as e:
                end = repo_timestamps[idx+m-1]

            print(f'from {start} to {end}')
            if upper_bound > start:
                temp2.append((upper_bound - start).days // 30)
            temp.append([start,end])
        d[repo_name] = sorted(temp2)
        all_found[repo_name] = temp

    for repo_name, patterns in all_found.items():
        print(repo_name)
        print(d[repo_name])
        for p in patterns:
            temp = issues_df.query('repo_fullname == @repo_name')
            num_created = len(temp.query('(created_at_ext > @p[0] and created_at_ext < @p[1])'))
            num_updated = len(temp.query('updated_at_ext > @p[0] and updated_at_ext < @p[1]'))
            num_opend = len(temp.query('created_at_ext < @p[1] and state == "open"'))
            num_closed = len(temp.query('created_at_ext < @p[1] and state == "closed"'))
            print(f'Issues : created {num_created}, updated {num_updated}, open {num_opend}, overall closed {num_closed}')
        print('\n')
