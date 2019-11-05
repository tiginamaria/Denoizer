import matplotlib.pyplot as plt
import librosa, librosa.display

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
