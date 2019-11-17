import scipy.io.wavfile
import numpy as np

from Visualiser import compare_magnitude, compare_spectrogram
from FilterUtils import import_signal, pump_signal

infile = 'samples/voice_with_car_noise.wav'
noisefile = 'samples/car_noise.wav'
outfile = 'samples/lms_filter_output.wav'

class LMSFilter(object):
    """Least Mean Squares adaptive filter"""
    def __init__(self, p=64, mu=1):
        """Initialization of the LMS filter
        :param p: filter size
        :param mu: learning rate
        """
        self.p = p
        self.mu = mu
        self.H = np.zeros(p)

    def filter(self, d, x):
        """Filters the data using an LMS adaptive filter scheme
        :param d: signal to be filtered
        :param x: noise signal
        """
        n = x.shape[0]
        x = np.concatenate((np.zeros(self.p), x))
        y = np.zeros(n)
        e = np.zeros(n)

        for i in range(n):
            j = i + self.p - 1
            x_i = np.flip(x[j - self.p + 1: j + 1])
            y[i] = self.H.dot(x_i)
            e[i] = d[i] - y[i]
            self.H += self.mu * e[i] * x_i
        return y, e


def main():
    # Import the audio from the file
    signal, sr, norm = import_signal(infile, 1000)

    noise, _, _ = import_signal(noisefile, 1000)
    noise = pump_signal(noise, len(signal))

    # Initialize the filter
    lms_filter = LMSFilter(mu=1, p=100)

    # Run filter on input audio
    error, filtered_signal = lms_filter.filter(signal, noise)

    # Export to wav to verify that the noise is gone
    scipy.io.wavfile.write(outfile, sr, filtered_signal * norm)

    # Visualise the difference
    compare_spectrogram("LMS filter", signal, filtered_signal, sr)
    compare_magnitude("LMS filter", signal, filtered_signal, sr)


if __name__ == '__main__':
    main()
