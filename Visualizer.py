import librosa, librosa.display
import matplotlib.pyplot as plt, IPython.display as ipd
import numpy as np
import seaborn as sns

sns.set()

def display_plots(title, x, amplitude_x, sr):
    plt.figure()
    ax1 = plt.subplot(2, 1, 1)
    amplitude_spectrum_plot(title, amplitude_x, sr)
    ax2 = plt.subplot(2, 1, 2)
    wave_plot(title, x, sr)
    plt.show()
    spectrogam_plot(title, amplitude_x)
    plt.show()

def spectrogam_plot(title, x):
    librosa.display.specshow(librosa.amplitude_to_db(x, ref = np.max), y_axis = 'log', x_axis = 'time')
    plt.grid(True)
    plt.title(title + ' power spectrogram')
    plt.colorbar(format='%+2.0f dB')
    plt.tight_layout()

def wave_plot(title, x, sr):
    ipd.Audio(x, rate=sr)
    plt.title(title)
    plt.ylabel('Amplitude')
    plt.xlabel('Time')
    plt.grid(True)
    time = np.arange(x.shape[0]) / sr
    plt.plot(time, x)
    # librosa.display.waveplot(x, sr=sr)

def amplitude_spectrum_plot(title, x, sr):
    x = np.mean(x, axis=1)
    plt.title(title + ' amplitude spectrum plot')
    plt.ylabel('Amplitude')
    plt.xlabel('Frequency')
    plt.plot(x.T)
