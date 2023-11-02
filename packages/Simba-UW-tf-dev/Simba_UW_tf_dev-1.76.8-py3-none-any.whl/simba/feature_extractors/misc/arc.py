import pandas as pd
from typing import List
try:
    from typing import Literal
except:
    from typing_extensions import Literal

import glob, os
from simba.mixins.train_model_mixin import TrainModelMixin
from simba.utils.read_write import read_df, get_fn_ext
from simba.utils.data import detect_bouts


def bout_aggregator(data_paths: List[str],
                    clfs: List[str],
                    aggregator: Literal['mean', 'median'],
                    min_bout_length: int,
                    fps: int):


    results = []
    for file_cnt, file_path in enumerate(data_paths):
        _, file_name, file_ext = get_fn_ext(filepath=file_path)
        df = read_df(file_path, file_type=file_ext[1:])
        bouts = detect_bouts(data_df=df, target_lst=clfs, fps=fps)
        bouts = bouts[bouts['Bout_time'] >= min_bout_length]
        for clf in clfs:
            other_clfs = [x for x in clfs if x is not clf]
            clf_bouts = bouts[bouts['Event'] == clf][['Start_frame', 'End_frame']].values
            for clf_bout in clf_bouts:
                clf_bout_data = df.loc[clf_bout[0]: clf_bout[1]].drop(clfs, axis=1)
                if aggregator is 'mean':
                    clf_bout_data = clf_bout_data.mean()
                if aggregator is 'median':
                    clf_bout_data = clf_bout_data.median()
                clf_bout_data[clf] = 1
                for clf in other_clfs:  clf_bout_data[clf] = 0
                clf_bout_data['START_FRAME'] = clf_bout[0]
                clf_bout_data['END_FRAME'] = clf_bout[1]
                clf_bout_data['VIDEO'] = file_name
                results.append(pd.DataFrame(clf_bout_data).T)
    print(pd.concat(results, axis=0).reset_index(drop=True))










        #print(bouts)








    #pass







data_paths = glob.glob('/Users/simon/Desktop/envs/troubleshooting/two_black_animals_14bp/project_folder/csv/targets_inserted' + '/*.csv')
bout_aggregator(data_paths=data_paths, clfs=['Attack', 'Sniffing'], aggregator='mean', min_bout_length=1.5, fps=10)











