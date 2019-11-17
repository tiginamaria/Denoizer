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
    :return original_signal: original audio signal
    :return filtered_signal: filtered audio signal
    :return sr: sampling rate
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

def compare_amplitudes(filter_type, original_audio, filtered_audio, sr):
    """Plots the spectrogram of the audio and the filtered audio signals in a subplot
    :param filter_type: type of used filter
    :return original_audio: original audio signal
    :return filtered_audio: filtered audio signal
    :return sr: sampling rate
    """
    plt.grid(True)
    plt.subplot(2, 1, 1)
    plt.title('Original')
    librosa.display.waveplot(x=original_audio, sr=sr)
    plt.subplot(2, 1, 2)
    plt.title('Filtered by ' + filter_type)
    librosa.display.waveplot(x=filtered_audio, sr=sr)
    plt.show()
    #
    # ipd.Audio(x, rate=sr)
    # plt.title(title)
    # plt.ylabel('Amplitude')
    # plt.xlabel('Time')
    # plt.grid(True)
    # time = np.arange(x.shape[0]) / sr
    # plt.plot(time, x)
    # # librosa.display.waveplot(x, sr=sr)

def amplitude_spectrum_plot(title, x, sr):
    x = np.mean(x, axis=1)
    plt.title(title + ' amplitude spectrum plot')
    plt.ylabel('Amplitude')
    plt.xlabel('Frequency')
    plt.plot(x.T)

def differense_plot(x, y):
    plt.plot(x, label='Input')
    plt.plot(y, label='Output')
    plt.show()
    librosa.display.waveplot(np.array([1, 2, 3]))


differense_plot(1, 1)
