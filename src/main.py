from utils import *
import numpy as np

if __name__ == '__main__':
    all_data = get_data()
    Ts = [v for _, v in all_data.items()]
    m = 14

    central_radius, central_Ts_idx, central_subseq_idx = consensus_motif(Ts, m)
    q = Ts[central_Ts_idx][central_subseq_idx:central_subseq_idx+m]

    print(q)
    for i in range(len(Ts)):
        print(search_pattern(Ts[i], q)[:2])
