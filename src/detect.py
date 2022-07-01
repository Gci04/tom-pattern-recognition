from utils import *
import numpy as np
from datetime import datetime
import json, sys, os
from argparse import ArgumentParser

def get_query_pattern(m, target_metric):
    data_path = f'../results/{target_metric}_result.json'
    assert os.path.isfile(data_path) , f'No consensus patterns for [{target_metric}!]'

    with open(data_path) as json_file:
        data = json.load(json_file)
    res = {}
    m_vals = [i for i in data.keys()]

    if str(m) in m_vals:
        temp = {}
        for thr, thr_data in data.get(str(m)).items():
            temp[thr] = thr_data.get('consensus_pattern')
        res[str(m)] = temp
    else :
        for j in m_vals:
            temp = {}
            for thr, thr_data in data.get(j).items():
                temp[thr] = thr_data.get('consensus_pattern')
            res[j] = temp
    return res
def read_repo_data(target_file, cols_to_select):
    result = {}
    repo_df = pd.read_csv(target_file, usecols=cols_to_select+['commit_datetime'], parse_dates=['commit_datetime'], index_col='commit_datetime')
    repo_df.sort_index(inplace=True)
    a = repo_df.index[-1] - repo_df.index[0]
    if a.days < 365//2 or repo_df.shape[0] < 50:
        print('Not enough commits to detect patterns')
        return None

    for target_metric in cols_to_select:
        result[target_metric] = repo_df[target_metric].values.astype(np.float64)

    return result

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-repo', required=True, help='Path to the repo data (.csv file)')
    parser.add_argument('-m', required=True, help='pattern size')
    parser.add_argument('-metric', '--target_metrics', nargs='+', default=['total_removed', 'total_added', 'total_changed'])
    args = parser.parse_args()
    assert os.path.isfile(args.repo) , f'[{args.repo}] does not exist'

    repo_data = read_repo_data(args.repo, args.target_metrics)

    for metric in args.target_metrics:
        consensus_p = get_query_pattern(args.m, metric)
        for m_found, m_data in consensus_p.items():
            for thr, cons in m_data.items():
                t = float(thr.split('-')[-1])
                found = search_pattern(repo_data[metric], cons, t)
                print(f'Found pattern : {*cons,}')
                print(f'Found {len(found)} times \n')
