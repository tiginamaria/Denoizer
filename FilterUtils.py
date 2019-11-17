import librosa, librosa.display
import numpy as np


def import_signal(filename, norm=1):
    """Imports a .wav file as a scaled float numpy array
    :param filename: audio's filename
    :return signal: imported signal from .wav
    :return sr: sampling rate
    :return norm: normalization coefficient
    """
    signal, sr = librosa.load(filename, sr=None, mono=True)
    signal /= norm
    return signal, sr, norm


def decompose(fft):
    """Decomposes fft of signal to magnitude spectrum nd phase spectrum
    :param fft: fft of signal
    :return magnitude: magnitude spectrum
    :return phase: phase spectrum
    """
    return np.abs(fft), np.angle(fft)


def pump_signal(signal, size):
    """Generate signal of given size by concatenating given signal
    :param signal: input signal
    :param size: desired signal size
    :return pumped_signal: pumped signal of given size
    """
    pumped_signal = signal
    while len(pumped_signal) < size:
        pumped_signal = np.concatenate((signal, signal))
    return pumped_signal[:size]
