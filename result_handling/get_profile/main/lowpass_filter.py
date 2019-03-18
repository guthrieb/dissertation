import numpy as np
from math import sin, pi
import sys
import scipy.signal as signal

def filter(data):
    N = 2
    Wn = 0.8
    B, A = signal.butter(N, Wn, output='ba')

    tempf = signal.filtfilt(B, A, data)

    return tempf