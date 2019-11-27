import librosa, librosa.display
import numpy as np
import scipy


def read_signal(filename, norm=1):
    """Read a .wav file as a scaled float numpy array
    :param filename: audio's filename
    :return signal: imported signal from .wav
    :return sr: sampling rate
    :return norm: normalization coefficient
    """
    signal, sr = librosa.load(filename, sr=None, mono=True)
    signal /= norm
    return signal, sr, norm


def write_signal(filename, signal, sr, norm=1):
    """Write a signal to .wav
    :param filename: audio's filename
    :param signal: signal to write into file
    :param sr: sampling rate
    :param norm: normalization coefficient
    """
    scipy.io.wavfile.write(filename, sr, signal * norm)


def decompose(fft):
    """Decomposes fft of signal to magnitude spectrum nd phase spectrum
    :param fft: fft of signal
    :return magnitude: magnitude spectrum
    :return phase: phase spectrum
    """
    return np.abs(fft), np.angle(fft)


def fit_size(signal, size):
    """Generate signal of given size by concatenating given signal
    :param signal: input signal
    :param size: desired signal size
    :return pumped_signal: pumped signal of given size
    """
    pumped_signal = signal
    while len(pumped_signal) < size:
        pumped_signal = np.concatenate((signal, signal))
    return pumped_signal[:size]
