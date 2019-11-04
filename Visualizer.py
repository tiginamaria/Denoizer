import librosa, librosa.display
import matplotlib.pyplot as plt

def wave_plot(title, x, sr):
    plt.grid(True)
    plt.title(title)
    plt.xlabel('amplitude')
    plt.ylabel('time (s)')
    plt.figure(figsize=(14, 5))
    librosa.display.waveplot(x, sr=sr)
    plt.show()

def amplitude_spectrum_plot(title, x, sr):
    plt.title(title + ' amplitude spectrum plot')
    plt.ylabel('amplitude')
    plt.xlabel('frequency')
    plt.plot(x.T)
    plt.show()
