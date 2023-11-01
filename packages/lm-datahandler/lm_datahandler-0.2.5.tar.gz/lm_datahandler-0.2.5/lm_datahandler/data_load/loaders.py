from datetime import datetime, timedelta

import numpy as np


def int_from_bytes_8bit(byte_arr):
    buffer = np.asarray(
        [1, 256, np.power(np.int64(256), 2), np.power(np.int64(256), 3), np.power(np.int64(256), 4),
         np.power(np.int64(256), 5), np.power(np.int64(256), 6), np.power(np.int64(256), 7)])

    res = byte_arr[0] * buffer[0] + byte_arr[1] * buffer[1] + byte_arr[2] * buffer[2] + byte_arr[3] * buffer[
        3] + \
          byte_arr[4] * buffer[4] + byte_arr[5] * buffer[5] + byte_arr[6] * buffer[6] + byte_arr[7] * buffer[7]
    return np.sum(res)


def int_from_bytes_4bit(byte_arr):
    buffer = np.asarray([1, 256, np.power(np.int64(256), 2), np.power(np.int64(256), 3)])

    res = byte_arr[0] * buffer[0] + byte_arr[1] * buffer[1] + byte_arr[2] * buffer[2] + byte_arr[3] * buffer[3]
    return np.sum(res)

class BaseLoader_X8(object):
    def __init__(self):
        pass

    def load_data(self, data_path):
        DataTotal = []
        PackageIDs = []
        self.file_data = open(data_path, 'rb')

        self.file_data_len = len(self.file_data.read())
        self.file_data.seek(0, 0)
        self.data_type = self.file_data.read(4)

        if self.data_type == b'ACC\x00':
            channel_count = 3
        elif self.data_type == b'EEG\x00':
            channel_count = 2

        self.file_data.seek(4, 0)
        self.version = int.from_bytes(self.file_data.read(4), byteorder='little', signed=False)

        self.file_data.seek(8, 0)
        self.length = int.from_bytes(self.file_data.read(4), byteorder='little', signed=False)

        self.file_data.seek(12, 0)
        self.device_type = int.from_bytes(self.file_data.read(4), byteorder='little', signed=False)

        self.file_data.seek(16, 0)
        self.point_bytes = int.from_bytes(self.file_data.read(1), byteorder='little', signed=False)
        self.file_data.seek(17, 0)
        self.packet_count = int.from_bytes(self.file_data.read(4), byteorder='little', signed=False)

        self.file_data.seek(21, 0)
        self.sample_count = int.from_bytes(self.file_data.read(4), byteorder='little', signed=False)

        self.file_data.seek(25, 0)
        self.origin_rate = int.from_bytes(self.file_data.read(4), byteorder='little', signed=False)

        self.file_data.seek(29, 0)
        self.sample_rate = int.from_bytes(self.file_data.read(4), byteorder='little', signed=False)

        self.file_data.seek(33, 0)
        self.start_time = int.from_bytes(self.file_data.read(8), byteorder='little', signed=False) / 1000

        self.file_data.seek(41, 0)
        self.end_time = int.from_bytes(self.file_data.read(8), byteorder='little', signed=False) / 1000

        if self.end_time < 24 * 3600:
            self.end_time = 24 * 3600

        self.start_time = datetime.fromtimestamp(self.start_time)
        self.end_time = datetime.fromtimestamp(self.end_time)

        self.file_data.seek(self.length, 0)
        all_packages = np.array(list(self.file_data.read(self.file_data_len - self.length)))
        package_length = self.sample_count * self.point_bytes * channel_count + 18
        all_packages = all_packages.reshape(-1, package_length)

        all_package_time = all_packages[:, 2:10]
        all_package_id = all_packages[:, 10:14]
        all_package_offset = all_packages[:, 14:18]
        all_package_data = all_packages[:, 18:package_length]

        # computing package loss rate/disconnection rate
        all_package_id = all_package_id.astype(np.uint8)
        all_package_id = np.apply_along_axis(int_from_bytes_4bit, axis=1, arr=all_package_id)
        all_package_id = all_package_id.astype(np.int32)

        all_package_time = all_package_time.astype(np.uint8)
        all_package_time = np.apply_along_axis(int_from_bytes_8bit, axis=1, arr=all_package_time)
        all_package_time = all_package_time.astype(np.int32)
        package_time_interval = all_package_time[1:] - all_package_time[:-1]
        disconnect_point = np.where(package_time_interval > 3000)[0]

        disconnection_sum = 0

        package_segment = [0]
        if disconnect_point is not None and len(disconnect_point) > 0:
            for i in range(len(disconnect_point)):
                package_segment.append(disconnect_point[i])
                package_segment.append(disconnect_point[i] + 1)
                disconnection_sum = all_package_time[disconnect_point[i] + 1] - all_package_time[disconnect_point[i]]

        self.disconnection_rate = disconnection_sum / all_package_time[-1]

        package_segment.append(all_package_id.shape[0] - 1)
        package_segment = np.array(package_segment).reshape([-1, 2])

        package_sum = 0
        loss_package_sum = 0
        for i in range(package_segment.shape[0]):
            left = package_segment[i][0]
            right = package_segment[i][1]
            package_sum += all_package_id[right] - all_package_id[left] + 1
            loss_package_sum += all_package_id[right] - all_package_id[left] + 1 - (right - left + 1)
        self.package_loss = loss_package_sum / package_sum

        # todo:做成可配置的
        # all_package_data = np.repeat(all_package_data, package_repeats, axis=0)

        all_package_data = all_package_data.reshape(-1, self.point_bytes)
        all_package_data = all_package_data[:, 0] + all_package_data[:, 1] * 256
        raw_data = np.squeeze(all_package_data)
        self.raw_data = np.transpose(raw_data.reshape([-1, channel_count]))

        data_total = all_package_data
        data_total = data_total[0:len(data_total) // channel_count * channel_count]
        data_total_T = data_total.reshape(-1, channel_count)
        self.data_total = []
        for i in range(channel_count):
            self.data_total.append(data_total_T[:, i])
        self.data_total = np.asarray(self.data_total)
        self.time_length = (self.end_time - self.start_time).total_seconds()


class BaseLoader(object):
    def __init__(self):
        pass



    def load_data(self, data_path):
        DataTotal = []
        PackageIDs = []
        self.file_data = open(data_path, 'rb')

        self.file_data_len = len(self.file_data.read())
        self.file_data.seek(0, 0)
        self.data_type = self.file_data.read(3)

        self.file_data.seek(4, 0)
        self.device_type = int.from_bytes(self.file_data.read(4), byteorder='little', signed=False)

        self.file_data.seek(12, 0)
        self.package_count = int.from_bytes(self.file_data.read(4), byteorder='little', signed=False)
        self.file_data.seek(16, 0)
        self.resolution = int.from_bytes(self.file_data.read(1), byteorder='little', signed=False)

        self.file_data.seek(21, 0)
        self.sampleRate = int.from_bytes(self.file_data.read(4), byteorder='little', signed=False)
        self.file_data.seek(81, 0)
        self.channel_data_length = int.from_bytes(self.file_data.read(4), byteorder='little', signed=False)

        self.file_data.seek(90, 0)
        self.data_offSet = int.from_bytes(self.file_data.read(4), byteorder='little', signed=False)
        self.file_data.seek(0, 0)


    # def _read_time_range(self):
        self.file_data.seek(30, 0)
        ST_Y = int.from_bytes(self.file_data.read(2), byteorder='little', signed=False)
        ST_M = int.from_bytes(self.file_data.read(1), byteorder='little', signed=False)
        ST_D = int.from_bytes(self.file_data.read(1), byteorder='little', signed=False)
        ST_H = int.from_bytes(self.file_data.read(1), byteorder='little', signed=False)
        ST_Min = int.from_bytes(self.file_data.read(1), byteorder='little', signed=False)
        ST_S = int.from_bytes(self.file_data.read(1), byteorder='little', signed=False)
        ST_ms = int.from_bytes(self.file_data.read(2), byteorder='little', signed=False)
        ST_D_more = 0
        if ST_H >= 24:
            ST_H = ST_H - 24
            ST_D_more = 1
        st_datetime = datetime(ST_Y, ST_M, ST_D, ST_H, ST_Min, ST_S, ST_ms)
        st_datetime = st_datetime + timedelta(days=ST_D_more)
        self.start_time = st_datetime



        self.file_data.seek(40, 0)
        ET_Y = int.from_bytes(self.file_data.read(2), byteorder='little', signed=False)
        if ET_Y > 2030:
            self.end_time = None
        else:
            ET_M = int.from_bytes(self.file_data.read(1), byteorder='little', signed=False)
            ET_D = int.from_bytes(self.file_data.read(1), byteorder='little', signed=False)
            ET_H = int.from_bytes(self.file_data.read(1), byteorder='little', signed=False)
            ET_Min = int.from_bytes(self.file_data.read(1), byteorder='little', signed=False)
            ET_S = int.from_bytes(self.file_data.read(1), byteorder='little', signed=False)
            ET_ms = int.from_bytes(self.file_data.read(2), byteorder='little', signed=False)
            ET_D_more = 0
            if ET_H >= 24:
                ET_H = ET_H - 24
                ET_D_more = 1
            et_datetime = datetime(ET_Y, ET_M, ET_D, ET_H, ET_Min, ET_S, ET_ms)
            et_datetime = et_datetime + timedelta(days=ET_D_more)
            self.end_time = et_datetime

        self.file_data.seek(0, 0)

class EEGLoader(BaseLoader):
    def __init__(self):
        super().__init__()
        self.data_total = None
        self.package_loss = None
        self.time_length = None
        self.raw_data = None
        # if sf_send == 10:
        self.package_length = 208
        self.package_std_time_interval = [100 - 20, 100, 100 + 20]
        # elif sf_send == 50:
        # self.package_length = 48
        # self.package_std_time_interval = [20-10, 20, 20+10]

    def load_data(self, data_path):
        super(EEGLoader, self).load_data(data_path)
        if self.package_count == 0:
            self.package_count = int((self.file_data_len - self.data_offSet) / self.package_length)
        # if self.device_type == 44:
        #     pass
        # else:
        #     self.package_std_time_interval = [70 - 20, 70, 70 + 20]
        self.file_data.seek(self.data_offSet, 0)

        all_packages = np.array(list(self.file_data.read(self.package_count * self.package_length)), dtype=np.int32).reshape(
            [-1, self.package_length])
        all_package_data = all_packages[:, 8:]
        raw_eeg = all_package_data.reshape([-1, self.resolution])
        raw_eeg = raw_eeg[:, 0] + raw_eeg[:, 1] * 256
        raw_eeg = np.squeeze(raw_eeg)
        self.raw_data = np.transpose(np.copy(raw_eeg.reshape([-1, 2])))


        all_package_ids = all_packages[:, 0:8]
        all_package_ids = np.apply_along_axis(int_from_bytes_8bit, 1, all_package_ids)
        package_time_intervals = all_package_ids[1:] - all_package_ids[0:-1]
        package_time_intervals = np.round(package_time_intervals / self.package_std_time_interval[1])
        package_time_intervals = np.insert(package_time_intervals, 0, [1])

        package_repeats = package_time_intervals.astype(np.int32)
        package_repeats[package_repeats <= 0] = 1

        self.time_length = np.sum(package_repeats)*0.1
        self.package_loss = (np.sum(package_repeats) - package_repeats.__len__()) / np.sum(package_repeats) * 100


        # todo: 做成可配置的
        all_package_data = np.repeat(all_package_data, package_repeats, axis=0)
        all_package_data = all_package_data.reshape([-1, self.resolution])

        all_package_data = all_package_data[:, 0] + all_package_data[:, 1] * 256
        all_package_data = np.squeeze(all_package_data)

        # package_loss_new = all_package_ids.shape[0] / total_time*10



        data_total = all_package_data
        data_total = data_total[0:len(data_total) // 2 * 2]
        data_total_T = data_total.reshape(-1, 2)
        self.data_total = []
        self.data_total.append(data_total_T[:, 0])
        self.data_total.append(data_total_T[:, 1])
        self.data_total = np.asarray(self.data_total)

        if self.end_time is None:
            self.end_time = self.start_time + timedelta(seconds=int(self.time_length))

        return self.raw_data, self.data_total, self.package_loss, self.time_length, self.start_time, self.end_time


class ACCLoader(BaseLoader):
    def __init__(self):
        super().__init__()
        # if sf_send == 10:
        self.package_length = 38
        self.package_std_time_interval = [100 - 20, 100, 100 + 20]
        # elif sf_send == 50:
        # self.package_length = 14
        # self.package_std_time_interval = [20-10, 20, 20+10]

    def load_data(self, data_path):
        super(ACCLoader, self).load_data(data_path)
        if self.package_count == 0:
            self.package_count = int((self.file_data_len - self.data_offSet) / self.package_length)
        # if self.device_type == 44:
        #     pass
        # else:
        #     self.package_std_time_interval = [70 - 20, 70, 70 + 20]
        self.file_data.seek(self.data_offSet, 0)
        all_packages = np.array(list(self.file_data.read(self.package_count * self.package_length))).reshape(
            [-1, self.package_length])
        all_package_data = all_packages[:, 8:]
        raw_acc = all_package_data.reshape([-1, self.resolution])
        raw_acc = raw_acc[:, 0] + raw_acc[:, 1] * 256
        raw_acc = np.squeeze(raw_acc)
        self.raw_data = np.transpose(np.copy(raw_acc.reshape([-1, 3])))


        all_package_ids = all_packages[:, 0:8]
        all_package_ids = np.apply_along_axis(int_from_bytes_8bit, 1, all_package_ids)
        package_time_intervals = all_package_ids[1:] - all_package_ids[0:-1]

        package_time_intervals = np.round(package_time_intervals / self.package_std_time_interval[1])
        package_time_intervals = np.insert(package_time_intervals, 0, [1])

        package_repeats = package_time_intervals.astype(np.int32)
        package_repeats[package_repeats <= 0] = 1

        self.time_length = np.sum(package_repeats)*0.1
        self.package_loss = (np.sum(package_repeats) - package_repeats.__len__()) / np.sum(package_repeats) * 100

        # todo: 做成可配置的
        all_package_data = np.repeat(all_package_data, package_repeats, axis=0)
        all_package_data = all_package_data.reshape([-1, self.resolution])

        # package_loss_new = all_package_ids.shape[0] / total_time*10

        all_package_data = all_package_data[:, 0] + all_package_data[:, 1] * 256
        all_package_data = np.squeeze(all_package_data)

        data_total = all_package_data
        data_total = data_total[0:len(data_total) // 3 * 3]
        data_total_T = data_total.reshape(-1, 3)
        self.data_total = []
        self.data_total.append(data_total_T[:, 0])
        self.data_total.append(data_total_T[:, 1])
        self.data_total.append(data_total_T[:, 2])
        self.data_total = np.asarray(self.data_total)

        if self.end_time is None:
            self.end_time = self.start_time + timedelta(seconds=int(self.time_length))

        return self.raw_data, self.data_total, self.package_loss, self.time_length, self.start_time, self.end_time

class STILoader(BaseLoader):
    def __init__(self):
        super(STILoader, self).__init__()
        self.package_length = 12
    def load_data(self, data_path):
        super(STILoader, self).load_data(data_path)

        if self.package_count == 0:
            self.package_count = int((self.file_data_len - self.data_offSet) / self.package_length)

        self.file_data.seek(self.data_offSet, 0)
        all_packages = np.array(list(self.file_data.read(self.package_count * self.package_length))).reshape(
            [-1, self.package_length])
        all_package_data = all_packages[:, 8:]
        # all_package_ids = all_packages[:, 0:8]

        all_package_data = all_package_data[:, 0] + all_package_data[:, 1] * 256 + all_package_data[:,
                                                                                   2] * 256 * 256 + all_package_data[
                                                                                                    :,
                                                                                                    3] * 256 * 256 * 256
        all_package_data = np.squeeze(all_package_data)
        self.data_total = all_package_data
        return self.data_total

    def load_sti_log(self, data_path):
        sti_index = []
        with open(data_path) as f:
            for line in f:
                if line.startswith("point count: "):
                    line = line.split("\t")[0]
                    index_str = line[13:]
                    sti_index.append(np.int32(index_str))
        sti_index = np.asarray(sti_index)
        return sti_index

class BLELoader(BaseLoader):
    def __init__(self):
        super().__init__()


    def load_data(self, data_path):
        super(BLELoader, self).load_data(data_path)

        total_length = len(self.file_data.read())
        self.file_data.seek(90, 0)
        offset = int.from_bytes(self.file_data.read(4), byteorder='little', signed=False)
        self.file_data.seek(offset, 0)
        ble_data = np.array(list(self.file_data.read(total_length - offset)))
        if ble_data.shape[0] == 0:
            return None

        ble_data = ble_data.reshape(-1, 16)
        # status = ble_data[:, 0:4]
        # status = np.apply_along_axis(int_from_bytes_4bit, 1, status)

        # package_id = ble_data[:, 4:8]
        # package_id = np.apply_along_axis(int_from_bytes_4bit, 1, package_id)

        sys_time = ble_data[:, 8:16]
        sys_time = np.apply_along_axis(int_from_bytes_8bit, 1, sys_time)

        disconnections = sys_time[0: sys_time.shape[0] // 2 * 2].reshape([-1, 2])
        drop_index = np.asarray([])
        for i in range(disconnections.shape[0]):
            if disconnections[i][1] - disconnections[i][0] > 12 * 24 * 3600 * 10000000:
                drop_index = np.append(drop_index, i).astype(np.int32)
        if drop_index.shape[0] != 0:
            disconnections = np.delete(disconnections, drop_index, axis=0)

        return disconnections
