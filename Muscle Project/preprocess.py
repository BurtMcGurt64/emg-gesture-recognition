import pandas as pd
import torch
import numpy as np
import matplotlib.pyplot as plt
import os
from scipy.signal import butter, filtfilt

# === Preprocessing ===
class Preprocessing:
    def __init__(self, data, fs=1000):
        self.data = np.copy(data)
        self.fs = fs    # so all functions can access the sampling frequency of the signal

        """
        Nyquist frequency: the maximum representable freequency is fs/2.
        Since fs=1000Hz (the data samples every ms), fs/2=500Hz.
        The highcut is 450Hz since muscle activity is maximum at that range, which is less than the Nyquist frequency.
        """
        self.nyquist = fs/2

    """
    apply a Butterworth bandpass filter to the input data

    3 types of filters
       1. Low-Pass: keeps low frequencies, removes high-frequency noise
       2. High-Pass: keeps high frequencies, removes motion artifacts and baseline drift
       3. Band-Pass: keeps frequencies within a certain range, removes both low and high extremes
     
    Why bandpass
        - Muscle activity is around 20-450 Hz
        - Frequencies <20Hz are most likely baseline drift
        - Frequencies >450Hz will contain noise from electrical equipment
    
    Why filtfilt
        - Standard filtering 'shifts' the signal horizontally so it becomes delayed
        - filtfilt applies the filter both forwards and backwards so it doesn't shift the signal

    parameters:
        data    - 1D array, which will be the EMG signal (samples)
        fs      - sampling rate in Hz
        lowcut  - low frequency cutoff in Hz
        highcut - high frequency cutoff in Hz
        order   - order of the filter (typically order=4)

    outputs:
        filtered_data - 1D array, bandpass filtered signal
    """
    def bandpass_filter(self, lowcut=20, highcut=450, order=4):
        # normalize the cutoff frequencies by dividing by nyquist frequency
        low_norm = lowcut / self.nyquist
        high_norm = highcut / self.nyquist

        # butter returns a rational function with numerator b and denominator a, so separate:
        b, a = butter(order, [low_norm, high_norm], btype='band', fs=self.fs)

        # apply filtfilt filter
        filtered_data = filtfilt(b, a, self.data)
        return filtered_data

    def normalize(self):
        data_min = np.min(self.data)
        data_max = np.max(self.data)
        normalized_data = (self.data - data_min) / (data_max - data_min + 1e-8)
        return normalized_data

    # CHANGE THE WINDOW SIZE AND STEP SIZE LATER BASED ON MY OWN DATA
    # EMG dataset - each gesture performed for 3 seconds, with 3 second pause between
    # rolling window is the most efficient
    # other method is to use: from sklearn.feature_extraction.image import view_as_windows
    def windowing(self, window_size=250, step_size=125):
        # loop through input data, splice into window_size
        # each iteration, add step_size to window_size
        windows = []
        features = []

        num_samples = self.data.shape[0]
        for start in range(0, num_samples - window_size + 1, step_size):
            window = self.data[start:start + window_size]
            windows.append(window)
            features.append(self.extract_features(window))

        return np.array(windows), np.array(features)
    
    def extract_features(self, window):
        # mean absolute value
        mav = np.mean(np.abs(window))

        # standard deviation
        std = np.std(window)

        # changes in slope/derivative
        diff1 = np.diff(window)
        slope_change = np.sum((diff1[:-1] * diff1[1:]) < 0)

        # zero crossings
        zero_crossing = np.sum(np.diff(np.sign(window)) != 0)

        return np.array([mav, std, slope_change, zero_crossing])