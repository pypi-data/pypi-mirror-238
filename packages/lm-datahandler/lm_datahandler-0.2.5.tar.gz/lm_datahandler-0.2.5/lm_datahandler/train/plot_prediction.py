import os.path

import matplotlib.pyplot as plt
from scipy.io import loadmat, savemat
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
import numpy as np
from sklearn.metrics import confusion_matrix


def plot_prediction_sleepstaging(targets, predictions, pp_predictions, save_path=None):
    f1 = f1_score(targets, predictions, average='weighted')
    accuracy = accuracy_score(targets, predictions)

    n3_target = np.zeros(targets.shape)
    n3_target[targets == 0] = 1
    n3_predictions = np.zeros(predictions.shape)
    n3_predictions[predictions == 0] = 1
    n3_f1 = f1_score(n3_target, n3_predictions)
    print("n3  f1: {}".format(n3_f1))

    n_target = np.zeros(targets.shape)
    n_target[targets == 1] = 1
    n_predictions = np.zeros(predictions.shape)
    n_predictions[predictions == 1] = 1
    n2_f1 = f1_score(n_target, n_predictions)
    print("n2  f1: {}".format(n2_f1))

    n_target = np.zeros(targets.shape)
    n_target[targets == 2] = 1
    n_predictions = np.zeros(predictions.shape)
    n_predictions[predictions == 2] = 1
    n1_f1 = f1_score(n_target, n_predictions)
    print("n1  f1: {}".format(n1_f1))

    rem_target = np.zeros(targets.shape)
    rem_target[targets == 3] = 1
    rem_predictions = np.zeros(predictions.shape)
    rem_predictions[predictions == 3] = 1
    rem_f1 = f1_score(rem_target, rem_predictions)
    print("rem  f1： {}".format(rem_f1))

    wake_target = np.zeros(targets.shape)
    wake_target[targets == 4] = 1
    wake_predictions = np.zeros(predictions.shape)
    wake_predictions[predictions == 4] = 1
    wake_f1 = f1_score(wake_target, wake_predictions)
    print("wake  f1： {}".format(wake_f1))

    plt.figure()
    plt.subplot(211)
    plt.plot(predictions)
    plt.plot(pp_predictions)
    plt.yticks([0, 1, 2, 3, 4], ['N3', 'N2', 'N1', 'REM', 'Wake'])
    # plt.subplot(312)
    # plt.yticks([0, 1, 2, 3, 4], ['N3', 'N1/N2', 'REM', 'Wake', 'Unwear'])
    plt.subplot(212)
    plt.plot(pp_predictions, label='prediction')
    plt.legend()
    plt.plot(targets, label='label')
    plt.legend()
    plt.yticks([0, 1, 2, 3, 4], ['N3', 'N2', 'N1', 'REM', 'Wake'])

    if save_path is not None:
        plt.savefig(save_path)

    print('accurancy: {}'.format(accuracy))
    print('f1: {}'.format(f1))


def plot_prediction_vs_targets(predictions, targets, save_path=None):
    f1 = f1_score(targets, predictions, average='weighted')
    accuracy = accuracy_score(targets, predictions)

    n3_target = np.zeros(targets.shape)
    n3_target[targets == 0] = 1
    n3_predictions = np.zeros(predictions.shape)
    n3_predictions[predictions == 0] = 1
    n3_f1 = f1_score(n3_target, n3_predictions)
    print("n3  f1: {}".format(n3_f1))

    n_target = np.zeros(targets.shape)
    n_target[targets == 1] = 1
    n_predictions = np.zeros(predictions.shape)
    n_predictions[predictions == 1] = 1
    n2_f1 = f1_score(n_target, n_predictions)
    print("n2  f1: {}".format(n2_f1))

    n_target = np.zeros(targets.shape)
    n_target[targets == 2] = 1
    n_predictions = np.zeros(predictions.shape)
    n_predictions[predictions == 2] = 1
    n1_f1 = f1_score(n_target, n_predictions)
    print("n1  f1: {}".format(n1_f1))

    rem_target = np.zeros(targets.shape)
    rem_target[targets == 3] = 1
    rem_predictions = np.zeros(predictions.shape)
    rem_predictions[predictions == 3] = 1
    rem_f1 = f1_score(rem_target, rem_predictions)
    print("rem  f1： {}".format(rem_f1))

    wake_target = np.zeros(targets.shape)
    wake_target[targets == 4] = 1
    wake_predictions = np.zeros(predictions.shape)
    wake_predictions[predictions == 4] = 1
    wake_f1 = f1_score(wake_target, wake_predictions)
    print("wake  f1： {}".format(wake_f1))

    plt.figure()
    plt.plot(predictions, label='prediction')
    plt.legend()
    plt.plot(targets, label='label')
    plt.legend()
    plt.yticks([0, 1, 2, 3, 4], ['N3', 'N2', 'N1', 'REM', 'Wake'])

    if save_path is not None:
        plt.savefig(save_path)

    print('accurancy: {}'.format(accuracy))
    print('f1: {}'.format(f1))


def plot_prediction_vs_targets_4_class(predictions, targets, save_path=None):
    epoch_to_drop = np.union1d(np.where(predictions == 5)[0], np.where(targets == 5)[0])
    predictions = np.delete(predictions, epoch_to_drop)
    targets = np.delete(targets, epoch_to_drop)

    f1 = f1_score(targets, predictions, average='weighted')
    accuracy = accuracy_score(targets, predictions)

    n3_target = np.zeros(targets.shape)
    n3_target[targets == 0] = 1
    n3_predictions = np.zeros(predictions.shape)
    n3_predictions[predictions == 0] = 1
    n3_f1 = f1_score(n3_target, n3_predictions)
    print("n3  f1: {}".format(n3_f1))

    n2_target = np.zeros(targets.shape)
    n2_target[targets == 1] = 1
    n2_predictions = np.zeros(predictions.shape)
    n2_predictions[predictions == 1] = 1
    n2_f1 = f1_score(n2_target, n2_predictions)
    print("n2  f1: {}".format(n2_f1))

    rem_target = np.zeros(targets.shape)
    rem_target[targets == 2] = 1
    rem_predictions = np.zeros(predictions.shape)
    rem_predictions[predictions == 2] = 1
    rem_f1 = f1_score(rem_target, rem_predictions)
    print("rem  f1： {}".format(rem_f1))

    wake_target = np.zeros(targets.shape)
    wake_target[targets == 3] = 1
    wake_predictions = np.zeros(predictions.shape)
    wake_predictions[predictions == 3] = 1
    wake_f1 = f1_score(wake_target, wake_predictions)
    print("wake  f1： {}".format(wake_f1))

    plt.figure()
    plt.plot(predictions, label='prediction')
    plt.legend()
    plt.plot(targets, label='label')
    plt.legend()
    plt.yticks([0, 1, 2, 3], ['N3', 'N2', 'REM', 'Wake'])

    if save_path is not None:
        plt.savefig(save_path)

    print('accurancy: {}'.format(accuracy))
    print('f1: {}'.format(f1))


def plot_prediction_N3Detection(targets, predictions, pp_predictions):
    f1 = f1_score(targets, predictions, average='weighted')
    accuracy = accuracy_score(targets, predictions)

    plt.figure()
    plt.subplot(211)
    plt.plot(predictions)
    plt.plot(pp_predictions)
    plt.yticks([0, 1], ['N123', 'Non-N'])
    # plt.subplot(312)
    # plt.yticks([0, 1, 2, 3, 4], ['N3', 'N1/N2', 'REM', 'Wake', 'Unwear'])
    plt.subplot(212)
    plt.plot(pp_predictions)
    plt.plot(targets)
    plt.yticks([0, 1], ['N123', 'Non-N'])

    print('accurancy: {}'.format(accuracy))
    print('f1: {}'.format(f1))


def plot_prediction_REMDetection(targets, predictions, pp_predictions):
    f1 = f1_score(targets, predictions, average='weighted')
    accuracy = accuracy_score(targets, predictions)

    plt.figure()
    plt.subplot(211)
    plt.plot(predictions)
    plt.plot(pp_predictions)
    plt.yticks([0, 1], ['REM', 'Non-REM'])
    # plt.subplot(312)
    # plt.yticks([0, 1, 2, 3, 4], ['N3', 'N1/N2', 'REM', 'Wake', 'Unwear'])
    plt.subplot(212)
    plt.plot(pp_predictions)
    plt.plot(targets)
    plt.yticks([0, 1], ['REM', 'Non-REM'])

    print('accurancy: {}'.format(accuracy))
    print('f1: {}'.format(f1))


def plotConfusionMatrix(prediction, target, class_count, labels, is_percentage, save_path=None):
    # class_count = 4  # 这个数值是具体的分类数，大家可以自行修改
    # labels = ['N3', 'N1/N2', 'REM', 'Wake']  # 每种类别的标签

    epoch_to_drop = np.union1d(np.where(prediction == 5)[0], np.where(target == 5)[0])
    prediction = np.delete(prediction, epoch_to_drop)
    target = np.delete(target, epoch_to_drop)

    cmatrix = confusion_matrix(target, prediction)
    plt.rcParams["font.family"] = ["sans-serif"]
    plt.rcParams["font.sans-serif"] = ['SimHei']
    plt.figure(figsize=(8, 6))
    # 显示数据
    plt.imshow(cmatrix, cmap=plt.cm.Reds)

    # 在图中标注数量/概率信息
    thresh = cmatrix.max() / 2  # 数值颜色阈值，如果数值超过这个，就颜色加深。
    for x in range(class_count):
        row_sum = np.sum(cmatrix, axis=1)
        for y in range(class_count):
            # 注意这里的matrix[y, x]不是matrix[x, y]
            info = int(cmatrix[y, x])
            if is_percentage:
                percentage = str(int(0 if row_sum[y] == 0 else cmatrix[y][x] / row_sum[y] * 10000) / 100)
                percentage += "%"
                plt.text(x, y, percentage,
                         verticalalignment='center',
                         horizontalalignment='center',
                         color="white" if info > thresh else "black")
            else:
                plt.text(x, y, info,
                         verticalalignment='center',
                         horizontalalignment='center',
                         color="white" if info > thresh else "black")

    # plt.tight_layout()  # 保证图不重叠
    # plt.title("澜猫自动分期 vs 专家分期", fontdict={'fontsize': 20})
    plt.yticks(range(class_count), labels, fontsize=12)
    plt.ylabel('Ground Truth from Experts Consensus', labelpad=10, fontdict={'fontsize': 15})
    plt.xlabel('LM Auto Sleep Staging', labelpad=10, fontdict={'fontsize': 15})
    plt.xticks(range(class_count), labels, fontsize=12)
    if save_path is not None:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')

def compute_and_plot_single_data():
    path = r"E:\dataset\X7-PSG\JZ_data\label_and_prediction\final_data\20230909_YCM247"
    fixed_label = loadmat(os.path.join(path, "hypno.mat"))['psg_trans_label'].squeeze()
    origin_label = loadmat(os.path.join(path, "psg_trans_label.mat"))['psg_trans_label'].squeeze()
    prediction = loadmat(os.path.join(path, "prediction_0.85.mat"))['prediction'].squeeze()

    min_length = min(fixed_label.shape[0], prediction.shape[0])
    # min_length = 1824
    fixed_label = fixed_label[:min_length]
    origin_label = origin_label[:min_length]
    prediction = prediction[:min_length]

    fixed_label[fixed_label == 2] = 1
    origin_label[origin_label == 2] = 1
    prediction[prediction == 2] = 1

    fixed_label[fixed_label == 3] = 2
    origin_label[origin_label == 3] = 2
    prediction[prediction == 3] = 2

    fixed_label[fixed_label == 4] = 3
    origin_label[origin_label == 4] = 3
    prediction[prediction == 4] = 3

    data_name = os.path.basename(path)
    savemat(os.path.join(r"E:\dataset\X7-PSG\JZ_data\label_and_prediction\4c_0.85", data_name + ".mat"),
            {
                "fixed_label": fixed_label,
                "origin_label": origin_label,
                "prediction": prediction
            })

    print("------------------ Fixed Targets vs Prediction ---------------------")
    plot_prediction_vs_targets_4_class(prediction, fixed_label, os.path.join(path, "prediction_vs_targets_fixed.png"))
    plotConfusionMatrix(prediction, fixed_label, 4, ['N3', 'N2', 'REM', 'Wake'], True,
                        os.path.join(path, "prediction_vs_targets_fixed_CM.png"))
    print("------------------ Origin Targets vs Prediction ---------------------")
    plot_prediction_vs_targets_4_class(prediction, origin_label, os.path.join(path, "prediction_vs_targets_origin.png"))
    plotConfusionMatrix(prediction, origin_label, 4, ['N3', 'N2', 'REM', 'Wake'], True,
                        os.path.join(path, "prediction_vs_targets_origin_CM.png"))



def compute_all_data():
    prediction = np.array([])
    origin_label = np.array([])
    fixed_label = np.array([])

    datas_path = r"E:\dataset\X7-PSG\JZ_data\label_and_prediction\4c_0.7"
    for data_name in os.listdir(datas_path):
        data = loadmat(os.path.join(datas_path, data_name))
        prediction = np.append(prediction, data["prediction"])
        origin_label = np.append(origin_label, data["origin_label"])
        fixed_label = np.append(fixed_label, data["fixed_label"])
    print("------------------ Fixed Targets vs Prediction ---------------------")
    plot_prediction_vs_targets_4_class(prediction, fixed_label, os.path.join(datas_path, "prediction_vs_targets_fixed.png"))
    plotConfusionMatrix(prediction, fixed_label, 4, ['N3', 'N2', 'REM', 'Wake'], True,
                        os.path.join(datas_path, "prediction_vs_targets_fixed_CM.png"))
    print("------------------ Origin Targets vs Prediction ---------------------")
    plot_prediction_vs_targets_4_class(prediction, origin_label, os.path.join(datas_path, "prediction_vs_targets_origin.png"))
    plotConfusionMatrix(prediction, origin_label, 4, ['N3', 'N2', 'REM', 'Wake'], True,
                        os.path.join(datas_path, "prediction_vs_targets_origin_CM.png"))

if __name__ == '__main__':
    compute_all_data()
