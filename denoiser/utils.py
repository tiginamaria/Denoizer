import os
import librosa
import numpy as np
from pydub import AudioSegment


def get_noise(signal, sr):
    """Get first two seconds of signal where noise is presented.
    :param filename: audio's filename
    :return signal: imported signal from .wav
    :return sr: sampling rate
    :return norm: normalization coefficient
    """
    return signal[:2 * sr]


def decompose(fft):
    """Decomposes fft of signal to magnitude spectrum nd phase spectrum.
    :param fft: fft of signal
    :return magnitude: magnitude spectrum
    :return phase: phase spectrum
    """
    return np.abs(fft), np.angle(fft)


def read_wav(filename, norm=1):
    """Read a .wav file as a scaled float numpy array.
    :param filename: audio's filename
    :return signal: imported signal from .wav
    :return sr: sampling rate
    :return norm: normalization coefficient
    """
    signal, sr = librosa.load(filename, sr=None, mono=True)
    signal /= norm
    return signal, sr, norm


def write_wav(filename, signal, sr):
    """Write a .wav from numpy array.
    :param filename: audio's filename
    :param signal: signal as numpy array
    :param sr: sampling rate
    """
    librosa.output.write_wav(filename, signal, sr)


def read_mp3(filename, norm=1):
    """Imports a .mp3 file as a scaled float numpy array.
    :param filename: audio's filename
    :return signal: imported signal from .wav
    :return sr: sampling rate
    :return norm: normalization coefficient
    """
    signal, sr = librosa.load(filename, sr=None, mono=True)
    signal /= norm
    return signal, sr, norm


def write_mp3(filename, signal, sr):
    """Write a .mp3 from numpy array.
    :param filename: audio's filename
    :param signal: signal as numpy array
    :param sr: sampling rate
    """
    wav_filename = filename.replace('.mp3', '.wav')
    write_wav(wav_filename, signal, sr)
    sound = AudioSegment.from_wav(wav_filename)
    sound.export(filename, format="mp3")
    os.system("rm -R {}".format(wav_filename))
#
# s0, r0, _ = read_mp3('audio/532993826.mp3')
# print(s0, r0)
# # s1, r1 = read('audio/voice_with_car_noise.wav')
# # s1, r1, _ = import_signal('audio/voice_with_car_noise.wav')
# # print(s1, r1)
#
# write_mp3('audio/0.mp3', s0, r0)
# # write('audio/1.wav', s1, r1)
