import numpy as np
import lightgbm as lgb
import pandas as pd
from lm_datahandler.postprocess.label_smooth import pp_label_smooth
import os

def sleep_staging_with_features(features, model_path, use_acc, use_time, context_mode=1):

    if model_path is not None:
        clf = lgb.Booster(model_file=model_path)
    else:
        model_name = "sleep_staging.txt"
        if use_acc:
            model_name = 'acc_' + model_name

        if use_time:
            model_name = 'time_' + model_name

        if context_mode == 2:
            model_name = "wholenight_" + model_name
        elif context_mode == 1:
            model_name = "realtime_" + model_name

        base_path = os.path.abspath(__file__)
        dir_path = os.path.dirname(base_path)
        dir_path = os.path.join(dir_path, "../models")
        clf = lgb.Booster(model_file=os.path.join(dir_path, model_name))

    feature_name = clf.feature_name()
    feature_for_predict = features[feature_name]
    raw_score = clf.predict(feature_for_predict)
    predictions = np.argmax(raw_score, axis=1)

    raw_n3 = np.where(predictions == 2)[0]
    excluded_n3 = raw_n3[np.where(raw_score[:, 2][raw_n3] < 0.75)[0]]
    predictions[excluded_n3] = 1

    raw_n1 = np.where(predictions == 0)[0]
    excluded_n1 = raw_n1[np.where(raw_score[:, 0][raw_n1] < 0.8)[0]]
    excluded_n1_to_wake = excluded_n1[np.where(raw_score[:, 4][excluded_n1] > raw_score[:, 3][excluded_n1])[0]]
    excluded_n1_to_rem = excluded_n1[np.where(raw_score[:, 4][excluded_n1] < raw_score[:, 3][excluded_n1])[0]]
    predictions[excluded_n1_to_wake] = 4
    predictions[excluded_n1_to_rem] = 3

    classes_with_alphabet_order = np.array(['N1', 'N2', 'N3', 'REM', 'Wake'])
    predictions = classes_with_alphabet_order[predictions]
    df_hypno = pd.Series(predictions)
    df_hypno.replace({'N3': 0, 'N2': 1, 'N1': 2, 'REM': 3, 'Wake': 4}, inplace=True)

    predictions = df_hypno.to_numpy()


    return predictions