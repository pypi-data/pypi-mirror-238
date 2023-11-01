from datetime import datetime

import joblib
import matplotlib.pyplot as plt
import pandas as pd
from lightgbm import LGBMClassifier
import lightgbm as lgb
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import train_test_split


def generate_dataset(data_path, use_eeg, use_acc, use_time, context_mode=2):
    df = pd.read_parquet(data_path)

    cols_all = df.columns
    if context_mode == 2:
        cols_time = cols_all[cols_all.str.startswith('time_')].tolist()
    else:
        cols_time = cols_all[cols_all.str.startswith('time_hour')].tolist()
    cols_eeg = cols_all[cols_all.str.startswith('eeg_')].tolist()
    cols_acc = cols_all[cols_all.str.startswith('acc_')].tolist()
    cols_demo = ['age', 'male', 'data_type']
    feature_columns = []
    if use_eeg:
        feature_columns = feature_columns + cols_eeg
    if use_acc:
        feature_columns = feature_columns + cols_acc
    if use_time:
        feature_columns = feature_columns + cols_time
    feature_columns = feature_columns + cols_demo
    X = df[feature_columns]
    y = df['stage']
    y.replace({0: 'N3', 1: 'N2', 2: 'N1', 3: 'REM', 4: 'Wake'}, inplace=True)
    # y.replace({0: 'N3', 1: 'N1/N2', 2: 'REM', 3: 'Wake', 4: 'Unwear'}, inplace=True)
    # y.value_counts(normalize=True).plot.barh(xlabel="Stage", ylabel="Proportion")
    return X, y


def train(train_data_path, validate_data_path, epoch, do_validate, use_eeg=True, use_acc=True, use_time=True,
          context_mode=2, algorithm=1):
    if use_eeg:
        name_part1 = 'eeg_'
    else:
        name_part1 = ''
    if use_acc:
        name_part2 = 'acc_'
    else:
        name_part2 = ''
    if use_time:
        name_part3 = 'time_'
    else:
        name_part3 = ''
    function = 'sleepstaging'
    if algorithm == 2:
        function = 'N3detection'
    elif algorithm == 3:
        function = 'REMdetection'
    if context_mode == 2:
        save_name = "wholenight_" + function + "_15s_" + name_part1 + name_part2 + name_part3 + str(
            epoch) + "iter_" + datetime.now().strftime('%Y%m%d_%H%M%S') + ".txt"
        outdir = "E:/githome/LightGBM_Sleep_Wholenight/saved/wholenight/"
    elif context_mode == 1:
        save_name = "realtime_" + function + "_15s_" + name_part1 + name_part2 + name_part3 + str(
            epoch) + "iter_" + datetime.now().strftime('%Y%m%d_%H%M%S') + ".txt"
        outdir = "E:/githome/lm_datahandler/lm_datahandler/train/"
    with open('model_name.txt', 'a') as f:
        f.write(outdir + save_name)
        f.write('\n')



    X_train, y_train = generate_dataset(train_data_path, use_eeg, use_acc, use_time, context_mode=context_mode)
    # X_test, y_test = generate_dataset(validate_data_path, use_eeg, use_acc, use_time, context_mode=context_mode)

    params = dict(
        boosting_type='gbdt',
        n_estimators=epoch,
        max_depth=4,
        num_leaves=15,
        colsample_bytree=0.5,
        importance_type='gain',
        n_jobs=4
    )

    if algorithm == 1:
        params['class_weight'] = {'N3': 3, 'N2': 1, 'N1': 20, 'REM': 1, 'Wake': 10}
        pass
    elif algorithm == 2:
        y_train.replace({'N1/N2': 'N123', 'N3': 'N123', 'REM': 'Non-N', 'Wake': 'Non-N'}, inplace=True)
        # y_test.replace({'N1/N2': 'N123', 'N3': 'N123', 'REM': 'Non-N', 'Wake': 'Non-N'}, inplace=True)
        params['class_weight'] = {'N123': 1, 'Non-N': 1}
        pass
    elif algorithm == 3:
        y_train.replace({'N1/N2': 'Non-REM', 'N3': 'Non-REM', 'REM': 'REM', 'Wake': 'Non-REM'}, inplace=True)
        # y_test.replace({'N1/N2': 'Non-REM', 'N3': 'Non-REM', 'REM': 'REM', 'Wake': 'Non-REM'}, inplace=True)
        params['class_weight'] = {'REM': 5, 'Non-REM': 1}
        pass
    elif algorithm == 4:
        pass

    # params['class_weight'] = 'balanced'

    # Fit
    clf = LGBMClassifier(**params)
    if do_validate:
        # X_train, _, y_train, _ = train_test_split(X_train, y_train, random_state=104, test_size=0.01, shuffle=True)
        # clf.fit(X_train, y_train, eval_set=(X_test, y_test), eval_metric=['logloss'])
        # acccurancy = accuracy_score(y_test, clf.predict(X_test))
        # f1 = f1_score(y_test, clf.predict(X_test), average='weighted')
        # print(f'Eval set: P: {acccurancy}, F1" {f1}.')
        # lgb.plot_metric(clf.evals_result_, metric='multi_logloss')

        X_train, X_test, y_train, y_test = train_test_split(X_train, y_train, random_state=104, test_size=0.1, shuffle=True)
        clf.fit(X_train, y_train, eval_set=(X_test, y_test), eval_metric=['logloss'])
        acccurancy = accuracy_score(y_test, clf.predict(X_test))
        f1 = f1_score(y_test, clf.predict(X_test), average='weighted')
        print(f'Eval set: P: {acccurancy}, F1" {f1}.')
        lgb.plot_metric(clf.evals_result_, metric='multi_logloss')

    else:
        clf.fit(X_train, y_train)

    print("training accuracy: %.3f" %
          (clf.score(X_train, y_train)))

    fname = outdir + save_name
    # Export model
    # joblib.dump(clf, fname, compress=True)
    clf.booster_.save_model(fname)

    df_imp = pd.Series(clf.feature_importances_, index=clf.feature_name_, name='Importance').round()
    df_imp.sort_values(ascending=False, inplace=True)
    df_imp.index.name = 'Features'
    df_imp.to_csv(fname[:-4] + ".csv")

    plt.show()
