import numpy as np
from scipy.io import loadmat
from scipy.signal import savgol_filter
import matplotlib.pyplot as plt

def sleep_posture_analyse(acc):
    acc_y = acc[1, :]
    acc_z = acc[2, :]

    cos = acc_z/np.sqrt(acc_z*acc_z + acc_y*acc_y)
    upper_grade = np.arccos(cos)
    grade = upper_grade*(acc_y/np.abs(acc_y))
    grade = savgol_filter(grade, window_length=50, polyorder=1)


    return grade


def turnover_count(acc, hypno, win=15, sf=50):
    assert acc.shape[0] == 3, "ACC should be a 3-D ndarray"
    assert acc.shape[1] % (win * sf) == 0, "The ACC length should be divisible by the epoch length"

    diff_acc = np.abs(acc[:, 1:] - acc[:, 0:-1])
    diff_acc = np.c_[diff_acc, [0, 0, 0]]

    avg_diff_acc = np.sum(np.reshape(np.sum(diff_acc, axis=0), [-1, sf * win]), axis=1) / (sf * win)
    # set max diff acc to 500
    avg_diff_acc[avg_diff_acc > 500] = 500
    normal_state = 100

    turnover = np.where(avg_diff_acc > normal_state)[0].shape[0]
    return turnover


if __name__ == '__main__':
    acc = loadmat(r"E:\dataset\dev_test_data\20230612_15927226341\acc.mat")
    grade = sleep_posture_analyse(acc)
    plt.plot(grade)
    plt.show()
