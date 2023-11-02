# !/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   Base 
@Time        :   2023/8/18 14:34
@Author      :   Xuesong Chen
@Description :   
"""
import re
import numpy as np
from pyedflib.edfreader import EdfReader


class Base:
    def __init__(self, file_path):
        self.reader = EdfReader(file_path)
        self.signal_labels = np.array(self.reader.getSignalLabels())
        self.duration = self.reader.getFileDuration()
        self._assign_signal_types()

    def _assign_signal_types(self):
        self.signal_type = []
        for idx, sig in enumerate(self.signal_labels):
            if re.search('E[CK]G', sig, re.IGNORECASE):
                self.signal_type.append('ecg')
            elif re.search('S[pa]O2', sig, re.IGNORECASE):
                self.signal_type.append('spo2')
            elif re.search('Effort ABD|ABDO', sig, re.IGNORECASE):
                self.signal_type.append('abd')
            elif re.search('CHEST|THOR', sig, re.IGNORECASE):
                self.signal_type.append('chest')
            elif re.search('EEG', sig, re.IGNORECASE):
                self.signal_type.append('eeg')
            elif re.search('EMG', sig, re.IGNORECASE):
                self.signal_type.append('emg')
            elif re.search('EOG', sig, re.IGNORECASE):
                self.signal_type.append('eog')
            elif re.search('Snore', sig, re.IGNORECASE):
                self.signal_type.append('snore')
            elif re.search('position', sig, re.IGNORECASE):
                self.signal_type.append('position')
            elif re.search('Flow', sig, re.IGNORECASE):
                self.signal_type.append('flow')
            else:
                self.signal_type.append('unk')
        self.signal_type = np.array(self.signal_type)

    def get_start_recording_time(self):
        return self.reader.getStartdatetime()

    def get_signal(self, ch_name=None, type='ecg', tmin=0, tmax=30, order=0):
        '''
        获取所有匹配信号，order代表次序，0代表第一个匹配的信号
        :param ch_name:
        :param type:
        :param tmin:
        :param tmax:
        :param order:
        :return:
        '''
        if ch_name:
            idx = np.argwhere(self.signal_labels == ch_name).flatten()[order]
        else:
            idx = np.argwhere(self.signal_type == type).flatten()[order]
        sfreq = int(self.reader.getSampleFrequency(idx))
        if tmin is None or tmax is None:
            return self.reader.readSignal(idx)
        start_samp_idx = sfreq * tmin
        end_samp_idx = sfreq * tmax
        n_samples = end_samp_idx - start_samp_idx
        return self.reader.readSignal(idx, start_samp_idx, n=n_samples)

    def get_sample_frequency(self, ch_name=None, type='ecg', order=0):
        # 注：只获取第一个匹配的信号
        if ch_name:
            idx = np.argwhere(self.signal_labels == ch_name).flatten()[order]
        else:
            idx = np.argwhere(self.signal_type == type).flatten()[order]
        return int(self.reader.getSampleFrequency(idx))

    def get_duration(self):
        return self.reader.file_duration


if __name__ == '__main__':
    fp = '/Users/cxs/project/OSAPillow/data/SHHS/edfs/shhs1-200001.edf'
    reader = Base(fp)
    sig = reader.get_signal(type='ecg')
    print(reader.signal_labels)
