from utils import *
import numpy as np
from datetime import datetime
import json, sys
from argparse import ArgumentParser

def approach1(Ts, p, z, d=0.3333):
    R = set()
    all_patterns = {}
    for m in np.arange(5,15):
        k = 0
        print(f'subsequence : {m}')
        central_radius, central_Ts_idx, central_subseq_idx = consensus_motif(Ts, m)
        consensus_pattern = Ts[central_Ts_idx][central_subseq_idx:central_subseq_idx+m]

        
        print(f'Consensus pattern : {*consensus_pattern,}')
        print(f'Radius {central_radius}')
        for ii, threshold in enumerate([central_radius/e for e in range(1,10)]):
            match_collection = {}
            k = 0
            for i in range(len(Ts)):
                distance_profile = search_pattern(Ts[i], consensus_pattern, max_distance=threshold)
                if distance_profile is None: continue
                tmatches = len(distance_profile)
                if tmatches > z and tmatches < 6:
                    match_collection[i] = distance_profile[:,1]
                    k += 1
            if k > 0 :
                pr = k/len(Ts)
                #print(threshold,pr)
                if pr > 0.05 and pr < 0.20:
                    print(f'threshold:{round(threshold,4)}, percentage: {round(pr,4)}')
                    all_patterns[m] = {}
                    all_patterns[m][f'threshold-{round(threshold,4)}'] = {}
                    all_patterns[m][f'threshold-{round(threshold,4)}']['consensus_pattern'] = consensus_pattern
                    all_patterns[m][f'threshold-{round(threshold,4)}']['patterns'] = match_collection
                    all_patterns[m][f'threshold-{round(threshold,4)}']['percentage'] = round(pr,4)

            if k < p and k > len(Ts)*0.05:
                print(f'adding : {*consensus_pattern,}')
                R.add(tuple(consensus_pattern))

    return R, all_patterns

def get_patterns(target_metric, all_data):
    Ts = []
    projects_names_map = {}
    i = 0
    for k, v in all_data.items():
        repo_timestamps = v.get('time_stamps')
        res = v.get(target_metric)
        if(len(res) > 15):
            Ts.append(res)
            projects_names_map[i] = k
            i+=1

    p = len(Ts)*0.25
    z = 4
    resultR, allPatterns = approach1(Ts, p, z, d=0.3333)

    if len(resultR) == 0: return None

    overall_result = {}
    for m, sub_data in allPatterns.items():
        subsequence_result = {}
        for thrshld, thrshld_sub_data  in sub_data.items():
            thrshld_result = {}
            for i, patterns_found in thrshld_sub_data['patterns'].items():
                repo_name = projects_names_map.get(i)
                temp = {}
                for n, p in enumerate(patterns_found,1):
                    temp[f'position {n}'] = [l.strftime('%Y-%m-%d %H:%M:%S') for l in all_data[repo_name]['time_stamps'][p:p+m]]
                thrshld_result[repo_name] = temp
            subsequence_result[thrshld] = thrshld_result
            subsequence_result[thrshld]['percentage'] = thrshld_sub_data['percentage']
            subsequence_result[thrshld]['consensus_pattern'] =  thrshld_sub_data['consensus_pattern'].tolist()
        overall_result[str(m)] = subsequence_result

    print('Saving result ...')
    with open(f'../results/{target_metric}_result.json', 'w') as fp:
        json.dump(overall_result, fp)

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-metric', '--target_metrics', nargs='+', default=['total_removed', 'total_added', 'total_changed'])
    args = parser.parse_args()
    print('Reading Data...')
    all_data = get_data(target_metrics=args.target_metrics)
    print('Finished reading data...')
    for metric in args.target_metrics:
        print(f'getting patterns for [{metric}]')
        get_patterns(metric, all_data)
