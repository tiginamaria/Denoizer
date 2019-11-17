import librosa, librosa.display
import matplotlib.pyplot as plt
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


def compare_spectrogram(filter_type, original_signal, filtered_signal, sr):
    """Plots the spectrogram of the audio and the filtered audio signals in a subplot
    :param filter_type: type of used filter
    :param original_signal: original audio signal
    :param filtered_signal: filtered audio signal
    :param sr: sampling rate
    """

    plt.subplot(1, 2, 1)
    plt.title('Original')
    plt.specgram(x=original_signal, Fs=sr)
    plt.axis(ymin=10, ymax=10000)
    plt.subplot(1, 2, 2)
    plt.title(filter_type)
    plt.specgram(x=filtered_signal, Fs=sr)
    plt.axis(ymin=10, ymax=10000)
    plt.show()


def compare_magnitude(filter_type, original_audio, filtered_audio, sr):
    """Plots magnitude of the audio and the filtered audio signals in a subplot
    :param filter_type: type of used filter
    :param original_audio: original audio signal
    :param filtered_audio: filtered audio signal
    :param sr: sampling rate
    """
    plt.grid(True)
    plt.subplot(2, 1, 1)
    plt.title('Original')
    librosa.display.waveplot(original_audio, sr=sr)
    plt.subplot(2, 1, 2)
    plt.title('Filtered by ' + filter_type)
    librosa.display.waveplot(filtered_audio, sr=sr)
    plt.show()

    plt.plot(original_audio, label='Input', color='r')
    plt.plot(filtered_audio, label='Output', color='b')
    plt.show()
