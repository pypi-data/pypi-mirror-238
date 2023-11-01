import matplotlib.pyplot as plt
import os

from lm_datahandler.datahandler import DataHandler
from scipy import signal
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.io import savemat, loadmat
from sklearn.metrics import f1_score, accuracy_score

from dataload_and_train import train
from lm_datahandler.train.post_process import pp_label_smooth
from plot_prediction import plot_prediction_sleepstaging, plot_prediction_N3Detection, plot_prediction_REMDetection, \
    plotConfusionMatrix, plot_prediction_vs_targets, plot_prediction_vs_targets_4_class
from predict import predict
import scipy.signal as sp_sig
from yasa import bandpower_from_psd_ndarray


# model_path_1 = 'saved/feature_experiment_2/wholenight_sleepstaging_15seeg4_700Iter_alldata20230111_182535.txt'
# model_path_1 = 'saved/feature_experiment_2/wholenight_sleepstaging_15s_eeg5_700Iter_alldata20230111_203907.txt'
# model_path_2 = 'saved/feature_experiment_2/wholenight_sleepstaging_eeg2_acc2_600Iter_alldata20230110_180724.txt'

def ButterFilter_2(data, fs, order=3, cutoff=0.5, model='highpass'):
    wn = 2 * cutoff / fs
    b, a = signal.butter(order, wn, model, analog=False)
    output = signal.filtfilt(b, a, data, axis=0)
    return output


def NotchFilter_2(data, order=3, notchFreq=[49, 51], fs=500, mode='bandstop'):
    w0 = notchFreq[0] / (fs / 2)
    w1 = notchFreq[1] / (fs / 2)
    b, a = signal.butter(order, [w0, w1], btype=mode, analog=False)
    output = signal.filtfilt(b, a, data, axis=0)
    return output


def model_predict(predict_data_path, algorithm):
    sf = 500
    # predictions_1, targets = predict(predict_data_path, sf, model_path=model_path, contains_acc=contains_acc)
    # predictions, targets = predict(predict_data_path, model_path=model_path, use_acc=use_acc, use_time=use_time,
    #                                context_mode=context_mode)
    data_handler = DataHandler()
    data_handler.load_data(data_name='temp_data', data_path=predict_data_path, patient_info=None)
    data_handler.preprocess(filter_param={'highpass': 0.5, 'lowpass': None, 'bandstop': [[49, 51]]})
    data_handler.save_data_to_mat(os.path.join(predict_data_path, "eeg_and_acc.mat"))
    # return
    data_handler.sleep_staging(use_acc=True)
    predictions = data_handler.sleep_staging_result

    targets_fixed = loadmat(os.path.join(predict_data_path, "hypno.mat"))['psg_trans_label']
    targets_origin = loadmat(os.path.join(predict_data_path, "psg_trans_label.mat"))['psg_trans_label']
    targets_fixed = np.array(targets_fixed).squeeze()
    targets_origin = np.array(targets_origin).squeeze()

    # targets = pd.Series(targets['epochs'])
    # targets.replace({"W ": 4, "N3": 0, "N2": 1, "N1": 2, "R ": 3}, inplace=True)
    # targets = targets.to_numpy()

    if algorithm == 1:
        # classes_with_alphabet_order = np.array(['N1', 'N2', 'N3', 'REM', 'Wake'])
        # predictions = classes_with_alphabet_order[predictions]
        # predictions = post_process.pp_label_smooth(predictions, window=10)
        df_hypno = pd.Series(predictions)
        df_hypno.replace({'N3': 0, 'N2': 1, 'N1': 2, 'REM': 3, 'Wake': 4}, inplace=True)
    elif algorithm == 2:
        classes_with_alphabet_order = np.array(['N123', 'Non-N'])
        predictions = classes_with_alphabet_order[predictions]
        # predictions = post_process.pp_label_smooth(predictions, window=10)
        df_hypno = pd.Series(predictions)
        df_hypno.replace({'N123': 0, 'Non-N': 1}, inplace=True)
    elif algorithm == 3:
        classes_with_alphabet_order = np.array(['REM', 'Non-REM'])
        predictions = classes_with_alphabet_order[predictions]
        # predictions = post_process.pp_label_smooth(predictions, window=10)
        df_hypno = pd.Series(predictions)
        df_hypno.replace({'REM': 0, 'Non-REM': 1}, inplace=True)

    predictions = df_hypno.to_numpy()
    # predictions = np.asarray([3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,3,3,3,3,3,3])

    # targets[targets == 5] = 4
    # predictions[predictions_2 == 3] = 3

    pp_predictions = pp_label_smooth(np.copy(predictions), window=2)
    abnormal_indices = np.union1d(np.where(pp_predictions == 5)[0], np.where(targets_fixed == 5)[0])
    pp_predictions = np.delete(pp_predictions, abnormal_indices)
    targets_origin = np.delete(targets_origin, abnormal_indices)
    targets_fixed = np.delete(targets_fixed, abnormal_indices)
    print(str(predict_data_path))

    # if algorithm == 1:
    #     print("-------------------Origin Targets---------------------")
    #     plot_prediction_vs_targets(pp_predictions, targets_origin,
    #                                save_path=os.path.join(predict_data_path, "prediction_vs_targets_origin.png"))
    #     plotConfusionMatrix(pp_predictions, targets_origin, 5, ['N3', 'N2', 'N1', 'REM', 'Wake'], True,
    #                         save_path=os.path.join(predict_data_path, "prediction_vs_targets_origin_CM.png"))
    #
    #     print("-------------------Fixed Targets---------------------")
    #     plot_prediction_vs_targets(pp_predictions, targets_fixed,
    #                                save_path=os.path.join(predict_data_path, "prediction_vs_targets_fixed.png"))
    #     plotConfusionMatrix(pp_predictions, targets_fixed, 5, ['N3', 'N2', 'N1', 'REM', 'Wake'], True,
    #                         save_path=os.path.join(predict_data_path, "prediction_vs_targets_fixed_CM.png"))

    pp_predictions[pp_predictions == 2] = 1
    targets_origin[targets_origin == 2] = 1
    targets_fixed[targets_fixed == 2] = 1

    pp_predictions[pp_predictions == 3] = 2
    targets_origin[targets_origin == 3] = 2
    targets_fixed[targets_fixed == 3] = 2

    pp_predictions[pp_predictions == 4] = 3
    targets_origin[targets_origin == 4] = 3
    targets_fixed[targets_fixed == 4] = 3


    if algorithm == 1:
        print("-------------------Origin Targets---------------------")
        plot_prediction_vs_targets_4_class(pp_predictions, targets_origin,
                                   save_path=os.path.join(predict_data_path, "prediction_vs_targets_origin.png"))
        plotConfusionMatrix(pp_predictions, targets_origin, 4, ['N3', 'N2', 'REM', 'Wake'], True,
                            save_path=os.path.join(predict_data_path, "prediction_vs_targets_origin_CM.png"))

        print("-------------------Fixed Targets---------------------")
        plot_prediction_vs_targets_4_class(pp_predictions, targets_fixed,
                                   save_path=os.path.join(predict_data_path, "prediction_vs_targets_fixed.png"))
        plotConfusionMatrix(pp_predictions, targets_fixed, 4, ['N3', 'N2', 'REM', 'Wake'], True,
                            save_path=os.path.join(predict_data_path, "prediction_vs_targets_fixed_CM.png"))



    # elif algorithm == 2:
    #     plot_prediction_N3Detection(targets, predictions, pp_predictions)
    # elif algorithm == 3:
    #     plot_prediction_REMDetection(targets, predictions, pp_predictions)

    # plt.show()

    # savemat(os.path.join(predict_data_path, 'prediction.mat'),
    #         {'prediction': pp_predictions, 'targets_origin': targets_origin, 'targets_fixed': targets_fixed})
    return pp_predictions, targets_origin, targets_fixed


def model_train(algorithm, context_mode):
    epoch = 120
    train_data_path = "E:/githome/lm_datahandler/lm_datahandler/train/insomnia_normal_students_eeg_acc_wholenight.parquet"
    # validate_data_path = "feature_data/insomnia_normal_students_eeg_acc_wholenight.parquet"
    # save_name = f"wholenight_eeg_acc_sleep_staging_{epoch}Iter_alldata_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    # save_name = "wholenight_" + "eeg_" + "sleep_staging_" + "1000Iter_" + "no_time_" + datetime.now().strftime('%Y%m%d_%H%M%S') + ".txt"

    train(train_data_path, None, epoch, do_validate=True, use_eeg=True, use_acc=True, use_time=False,
          algorithm=algorithm, context_mode=context_mode)


# 实时预测场景中，使用p8/p4（单位为epoch，不是分钟）等往期小窗口平均作为特征的预测效果较差，但仿照整夜分析的方案，使用P15则效果上升
# 使用P15时，P15(t=0) = C15(t=-7)，即相当于延迟版的整夜分析
# 因此，效果能够和整夜分析的效果类似，但是存在1~2分钟的延迟

def main():
    # feature_generation(context_mode=2)

    """
    algorithm for training:
    1. Sleep Staging
    2. N3(12) Detection
    3. REM Detection
    4. Sober Detection
    """
    # model_train(algorithm=1, context_mode=2)

    with open('model_name.txt', 'r') as f:
        model_path_1 = list(f.readlines())[-1].strip()
    predict_data_path = [
        r"E:\dataset\X7-PSG\JZ_data\20230520\20230520_WZY",
        r"E:\dataset\X7-PSG\JZ_data\20230526\20230526_LTY",
        r"E:\dataset\X7-PSG\JZ_data\20230602\20230602_CM",
        r"E:\dataset\X7-PSG\JZ_data\20230603\20230603_DL",
        r"E:\dataset\X7-PSG\JZ_data\20230630\15939662980_0630-20_21_33_0701-06_51_10_0.05_4",
        r"E:\dataset\X7-PSG\JZ_data\20230708\20230708_213324_YCM146V0",
        r"E:\dataset\X7-PSG\JZ_data\20230714\20230714_221325_YCM191V0",
        r"E:\dataset\X7-PSG\JZ_data\20230722\20230722_212527_YCM212V0",
        r"E:\dataset\X7-PSG\JZ_data\20230728\20230728_214445_YCM205V0",
        r"E:\dataset\X7-PSG\JZ_data\20230729\20230729_211300_YCM207V0",
        r"E:\dataset\X7-PSG\JZ_data\20230805\20230805_213247_YCM200V0",
        r"E:\dataset\X7-PSG\JZ_data\20230825\18198578652_0825-20_25_14_0826-03_14_35_1.44_5",
        r"E:\dataset\X7-PSG\JZ_data\20230825\18198578652_0825-21_01_37_0826-07_49_07_0.04_5",
        r"E:\dataset\X7-PSG\JZ_data\20230826\15927226341_0826-21_03_04_0827-07_01_56_0.13_5",
        r"E:\dataset\X7-PSG\JZ_data\20230826\15927226341_0826-21_07_54_0827-07_21_26_0.00_5",
        r"E:\dataset\X7-PSG\JZ_data\20230901\18198578652_0901-21_27_18_0902-07_18_45_0.02_5",
        r"E:\dataset\X7-PSG\JZ_data\20230902\15927226341_0902-21_35_03_0903-07_17_50_0.00_5",
        r"E:\dataset\X7-PSG\JZ_data\20230902\15927226341_0902-21_38_31_0903-07_17_26_0.60_5",
        r"E:\dataset\X7-PSG\JZ_data\20230909\18198578652_0909-20_56_37_0910-07_24_00_1.20_5"
    ]
    pp_predictions = np.array([0])
    targets_origin = np.array([0])
    targets_fixed = np.array([0])
    for data in predict_data_path:
        temp_predictions, temp_targets_origin, temp_targets_fixed = model_predict(data, 1)
        pp_predictions = np.concatenate((pp_predictions, temp_predictions))
        targets_origin = np.concatenate((targets_origin, temp_targets_origin))
        targets_fixed = np.concatenate((targets_fixed, temp_targets_fixed))
    print("-------------------Total: Origin Targets---------------------")
    plot_prediction_vs_targets_4_class(pp_predictions, targets_origin)
    print("-------------------Total: Fixed Targets---------------------")
    plot_prediction_vs_targets_4_class(pp_predictions, targets_fixed)


if __name__ == "__main__":
    # get_relative_spectral_power()
    # plot_psg_x7_staging()
    main()
    # plt.colormaps()
    # plt.show()
