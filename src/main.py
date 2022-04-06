import numpy as np
import pandas as pd
import random

# for data visualization
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# For data preprocessing
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split

import matplotlib.pyplot as plt

# For matrix profile calculations
import stumpy

def main(data_path = '../Data/repositories.csv'):
    cols_to_select = ['commit_datetime', 'full_name', 'total_files', 'total_added','total_removed','total_changed']
    repository_hist_df = pd.read_csv(data_path, usecols= cols_to_select,\
                                     parse_dates=['commit_datetime'],index_col='commit_datetime')

    repo_to_select = "TalkingPotatoTeam/farming_server"
    df = repository_hist_df.query('full_name == @repo_to_select').sort_index()
    df.drop('full_name',axis=1,inplace=True)
    col_mapping = {'total_files': 'T1', 'total_added': 'T2','total_removed':'T3',
                  'total_changed':'T4'}
    df.rename(col_mapping, axis=1,inplace=True)
    df.index = np.arange(0,len(df))
    print(df.head())
    

if __name__ == '__main__':
    main()
