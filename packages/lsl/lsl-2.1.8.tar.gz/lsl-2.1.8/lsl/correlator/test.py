import numpy as np
import scipy
from scipy.signal import firwin, freqz, lfilter

def generate_win_coeffs(M, P, window_fn="hamming"):
    win_coeffs = scipy.signal.get_window(window_fn, M*P)
    sinc       = scipy.signal.firwin(M * P, cutoff=1.0/P, window="rectangular")
    sinc /= sinc.max()
    win_coeffs *= sinc
    return win_coeffs


M = 8
P = 32

for i,v in enumerate(generate_win_coeffs(M, P, "hamming")):
    print(f"{i}: {v}")
