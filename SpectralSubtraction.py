import numpy as np
import scipy
import Visualizer
import librosa.display

# edit following wav file name
infile = 'samples/voice_with_car_noise.wav'
outfile = 'samples/output_short.wav'
noisefile = 'samples/car_noise.wav'

# load input file, and stft (Short-time Fourier transform)
print('load wav', infile)
x, sr = librosa.load(infile, sr=None, mono=True) # load audio file with noise as: x[t] - discrete signal and sr - sampling rate
fft_x = librosa.stft(x)         # Short-time Fourier transform
x_amplitude_sp = np.abs(fft_x)  # get audio amplitude spectrum
Visualizer.amplitude_spectrum_plot("Input audio", x_amplitude_sp, sr)
x_phase_sp = np.angle(fft_x)    # get audio phase spectrum

# load noise file, and stft (Short-time Fourier transform)
print('load wav', noisefile)
noise, noise_sr = librosa.load(noisefile, sr=None, mono=True)
fft_noise = librosa.stft(noise)
noise_amplitude_sp = np.abs(fft_noise)  # get audio amplitude spectrum
Visualizer.amplitude_spectrum_plot("Input audio", noise_amplitude_sp, sr)
noise_footprint = np.mean(noise_amplitude_sp, axis=1) # get mean noise amplitude

# calculate output audio signal with istft (Inverse short-time Fourier transform)
y_amplitude_sp = x_amplitude_sp - noise_footprint.reshape((noise_footprint.shape[0], 1))  # reshape for broadcast to subtract
fft_y = y_amplitude_sp * np.exp(1.0j * x_phase_sp) # apply phase information
y = librosa.istft(fft_y) # back to time domain signal

# save as a wav file
scipy.io.wavfile.write(outfile, sr, (y * 32768).astype(np.int16))
print('write wav', outfile)
