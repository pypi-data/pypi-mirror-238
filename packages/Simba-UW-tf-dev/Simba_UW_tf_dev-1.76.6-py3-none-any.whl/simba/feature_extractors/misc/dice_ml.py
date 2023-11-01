import dice_ml
import pandas as pd
import numpy as np

model_path = '/Users/simon/Desktop/envs/troubleshooting/two_black_animals_14bp/models/Attack.sav'
data_path = '/Users/simon/Desktop/envs/troubleshooting/two_black_animals_14bp/project_folder/csv/features_extracted/temp/Together_1.csv'

data_df = pd.read_csv(data_path, index_col=0).head(10).iloc[:, 0:587]
feature_names = list(data_df.columns)
data_df['target'] = np.random.random_integers(0, 1, len(data_df))


d = dice_ml.Data(dataframe=data_df, continuous_features=feature_names, outcome_name='target')
m = dice_ml.Model(model_path=model_path,
                  backend='sklearn',
                  func="ohe-min-max")

exp = dice_ml.Dice(d, m, method="random")

test_df = data_df.drop(['target'], axis=1)

e1 = exp.generate_counterfactuals(test_df[0:1], total_CFs=2, desired_class="opposite")