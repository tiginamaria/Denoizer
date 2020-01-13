import numpy as np
import librosa

from denoiser.utils import read_mp3, write_mp3, read_wav, write_wav, get_noise, decompose
from denoiser.visualiser import compare_spectrogram, compare_magnitude

class SSFilter(object):
    """Spectral Subtraction filter"""

    def run(self, infile, outfile, format):
        if format == 'mp3':
            read = read_mp3
            write = write_mp3
        elif format == 'wav':
            read = read_wav
            write = write_wav
        else:
            print('Unsupported file format(only .wav .mp3)')
            return
        signal, sr, _ = read(infile)
        noise = get_noise(signal, sr)
        filtered_signal = self.filter(signal, noise)
        write(outfile, filtered_signal, sr)

    def filter(self, signal, noise):
        """Filters the signal using Spectral subtraction algorithm
        :param signal: signal to denoise
        :param noise: noise signal
        :return filtered_signal: filtered signal
        """

        # Apply Short-time Fourier transform to signal
        fft_signal = librosa.stft(signal)
        signal_magnitude, signal_phase = decompose(fft_signal)

        # Apply Short-time Fourier transform to noise signal
        fft_noise = librosa.stft(noise)
        noise_magnitude, _ = decompose(fft_noise)
        # Get mean noise amplitude
        noise_footprint = np.mean(noise_magnitude, axis=1)

        # Calculate output magnitude spectrum
        filtered_audio_magnitude = (signal_magnitude - noise_footprint.reshape((noise_footprint.shape[0], 1))).clip(0.)
        # Add phase information
        fft_filtered_signal = filtered_audio_magnitude * np.exp(1.0j * signal_phase)
        # Apply Inverse short-time Fourier transform to return back to time domain signal
        filtered_signal = librosa.istft(fft_filtered_signal)

        return filtered_signal
