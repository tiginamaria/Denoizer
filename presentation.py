import numpy as np
import matplotlib.pyplot as plt
import librosa
np.random.seed(0)


def sine(X, frequency=200.):
    """Generate clean sine wave
    :param X: array of time
    :param frequency: wave's frequency
    """
    return np.sin(2 * np.pi * (X) / frequency)


def noisy(Y, noise_range=(-0.35, 0.35)):
    """Add noise to wave
    :param Y: array of wave's amplitudes
    :param noise_range: biases for generated noise
    :return noised signal
    """
    noise = np.random.uniform(noise_range[0], noise_range[1], size=Y.shape)
    return Y + noise


def sample(amplitude, frequency, len, phase=0, title=False):
    """Generate sample with noise
    :param amplitude: array of waves' amplitudes
    :param phase: array of waves' phases
    :param frequency: array of waves' frequencies
    :param len: length of sample
    :param title: if True return sample equation
    :return wave sample with given parameters
    """
    X = np.arange(len)
    s = amplitude * sine(X + phase / 360 * frequency, frequency)
    if title:
        return s, "{0:.2f} * sin(t * 2 * pi / {0:.2f} + {0:.2f})"\
            .format(amplitude, frequency, phase / 360 * frequency)
    return s


def noisy_sample(amplitude, frequency, len, phase=0):
    """Generate sample with noise
    :param amplitude: array of waves' amplitudes
    :param phase: array of waves' phases
    :param frequency: array of waves' frequencies
    :param len: length of sample
    """
    s = sample(amplitude, frequency, len, phase)
    return noisy(s)


def draw_discretization(sample, sr, title):
    """Plots waves' discrete signal
    :param sample: array of amplitudes
    :param sr: sample rate
    :param title: title for plot
    """
    discretization = [[sample[i // sr]] for i in range(len(sample) * sr)]
    discretization = [x if i % sr == 0 else [0] for i, x in enumerate(discretization)]
    plt.plot(np.array(discretization))
    plt.xlabel("Time (s) * sampling rate (1 / s)")
    plt.ylabel("Amplitude")
    plt.title(title)
    plt.legend()
    plt.show()


def draw_waves(amplitudes, phases, frequensies, len):
    """Plots waves with given amplitudes and frequencies
    :param amplitudes: array of waves' amplitudes
    :param phases: array of waves' phases
    :param frequencies: array of waves' frequencies
    :param title: plot title
    """
    signal = np.array([0. for _ in range(len)])
    title = []
    for a, f, p in zip(amplitudes, frequensies, phases):
        s, t = sample(a, f, len, p, True)
        signal += s
        title.append(t)
    plt.axhline(0, color='black')
    plt.plot(np.array(signal))
    plt.ylim(-max(amplitudes) - 1, max(amplitudes) + 1)
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.title(" + ".join(title))
    plt.legend()
    plt.show()


def draw_phase(phases, frequencies, title):
    """Plots phase spectrum for waves with given amplitudes and frequencies
    :param phases: array of waves' phases
    :param frequencies: array of waves' frequencies
    :param title: plot title
    """
    max_frequency = int(max(frequencies)) + 100
    s = [[0] for _ in range(max_frequency)]
    for p, f in zip(phases, frequencies):
        s[f] = [p]
    plt.plot(np.array(s))
    plt.ylim(0, 160)
    plt.xlabel("Frequensy (Hz)")
    plt.ylabel("Phase")
    plt.title(title)
    plt.legend()
    plt.show()


def draw_amplitude_spectrum(amplitudes, frequencies, title):
    """Plots amplitude spectrum for waves with given amplitudes and frequencies
    :param amplitudes: array of waves' amplitudes
    :param frequencies: array of waves' frequencies
    :param title: plot title
    """
    max_frequency = int(max(frequencies)) + 100
    s = [[0] for _ in range(max_frequency)]
    for a, f in zip(amplitudes, frequencies):
        s[f] = [a]
    plt.plot(np.array(s))
    plt.axis(ymin=0, ymax=9)
    plt.xlabel("Frequensy (Hz)")
    plt.ylabel("Amplitude")
    plt.title(title)
    plt.legend()
    plt.show()


def draw_spectrum(filename, title):
    """Plots the amplitudes of the audio
    :param filename: name of  audio file
    :param title: title for plot
    """
    s, sr = librosa.load(filename, sr=16000)
    f = np.fft.rfft(s)
    plt.xlim(0, 20000)
    plt.plot(f)
    plt.xlabel("Frequensy (Hz)")
    plt.ylabel("Amplitude")
    plt.title(title)
    plt.legend()
    plt.show()


def audio_amplitudes(filename, title):
    """Plots the amplitudes of the audio
    :param filename: name of  audio file
    :param title: title for plot
    """
    s, sr = librosa.load(filename, sr=16000)
    plt.plot(s)
    plt.xlabel("Time (s) * sampling rate (1 / s)")
    plt.ylabel("Amplitude")
    plt.title(title + " sr={}".format(sr))
    plt.legend()
    plt.show()


def spectrogram(filename, title):
    """Plots the spectrogram of the audio
    :param filename: name of  audio file
    :param title: title for plot
    """
    s, sr = librosa.load(filename, sr=16000)
    plt.specgram(x=s, Fs=sr)
    plt.xlabel("Time (s)")
    plt.ylabel("Frequensy (Hz)")
    plt.axis(ymin=10, ymax=10000)
    plt.title(title + " sr={}".format(sr))
    plt.legend()
    plt.show()
