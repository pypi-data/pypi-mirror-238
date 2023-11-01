import os

import joblib
import mne
import numpy as np
import lightgbm as lgb
import pandas as pd


from lm_datahandler.train.mat_to_npz_new import new_datahandler_load_mat


def predict(data_path, model_path, use_acc, use_time, context_mode):
    # raw = np.load(data_path)
    # raw_eeg = raw["x"]
    # # raw_acc = None
    # raw_acc = raw["acc"]
    # person_info = dict(age=30, male=1)
    #
    # # create and select features
    # X = RSCEEGFeature(person_info, raw_eeg, 500, raw_acc, 50, context_mode=2, data_type=data_type).get_features()

    X, targets = new_datahandler_load_mat(data_path)

    cols_all = X.columns
    if context_mode == 2:
        cols_time = cols_all[cols_all.str.startswith('time_')].tolist()
    else:
        cols_time = cols_all[cols_all.str.startswith('time_hour')].tolist()
    cols_acc = cols_all[cols_all.str.startswith('acc_')].tolist()
    cols_eeg = cols_all[cols_all.str.startswith('eeg_')].tolist()
    cols_demo = ['age', 'male', 'data_type']
    features = []
    features = features + cols_eeg
    if use_acc:
        features = features + cols_acc
    if use_time:
        features = features + cols_time
    features = features + cols_demo
    X = X[features]

    # # Predict with joblib model
    # clf = joblib.load(model_path)
    # predictions = clf.predict(X)

    # Predict with txt Booster model

    # X.to_csv('feature.csv', index=None)
    clf = lgb.Booster(model_file=model_path)
    predictions = clf.predict(X)

    predictions = np.argmax(predictions, axis=1)


    return predictions, targets




