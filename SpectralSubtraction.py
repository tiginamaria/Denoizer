import numpy as np
import scipy
import librosa

from FilterUtils import import_signal
from Visualiser import compare_spectrogram, compare_magnitude

infile = 'samples/voice_with_car_noise.wav'
noisefile = 'samples/car_noise.wav'
outfile = 'samples/output_short.wav'


class SSFilter(object):
    """Spectral Subtraction filter"""

    def decompose(self, fft):
        """Decomposes fft of signal to magnitude spectrum nd phase spectrum
        :param fft: fft of signal
        :return magnitude: magnitude spectrum
        :return phase: phase spectrum
        """
        return np.abs(fft), np.angle(fft)

    def filter(self, signal, noise):
        """Filters the signal using Spectral subtraction algorithm
        :param signal: signal to denoise
        :param noise: noise signal
        :return filtered_signal: filtered signal
        """

        # Apply Short-time Fourier transform to signal
        fft_signal = librosa.stft(signal)
        signal_magnitude, signal_phase = SSFilter.decompose(self, fft_signal)

        # Apply Short-time Fourier transform to noise signal
        fft_noise = librosa.stft(noise)
        noise_magnitude, _ = SSFilter.decompose(self, fft_noise)
        # Get mean noise amplitude
        noise_footprint = np.mean(noise_magnitude, axis=1)

        # Calculate output magnitude spectrum
        filtered_audio_magnitude = (signal_magnitude - noise_footprint.reshape((noise_footprint.shape[0], 1))).clip(0.)
        # Add phase information
        fft_filtered_signal = filtered_audio_magnitude * np.exp(1.0j * signal_phase)
        # Apply Inverse short-time Fourier transform to return back to time domain signal
        filtered_signal = librosa.istft(fft_filtered_signal)

        return filtered_signal


def main():
    # Load input file
    signal, sr, _ = import_signal(infile, 1)

    # Load noise file
    noise, noise_sr, _ = import_signal(noisefile, 1)

    # Apply filter
    ss_filter = SSFilter()
    filtered_signal = ss_filter.filter(signal, noise)

    # Save filtered signal as a wav file
    scipy.io.wavfile.write(outfile, sr, (filtered_signal * 32768).astype(np.int16))

    # Visualise the difference
    compare_spectrogram("Spectral Subtraction filter", signal, filtered_signal, sr)
    compare_magnitude("Spectral Subtraction filter", signal, filtered_signal, sr)


if __name__ == '__main__':
    main()
