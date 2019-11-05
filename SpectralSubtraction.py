import numpy as np
# import scipy
import scipy

import Visualizer
import librosa.display

# edit following wav file name
infile = 'samples/la.wav'
outfile = 'samples/output_short.wav'
noisefile = 'samples/car_noise_2.wav'

# load input file, and stft (Short-time Fourier transform)
print('load wav', infile)
x, sr = librosa.load(infile, sr=None, mono=True) # load audio file with noise as: x[t] - discrete signal and sr - sampling rate
fft_x = librosa.stft(x)         # Short-time Fourier transform
x_amplitude_sp = np.abs(fft_x)  # get audio amplitude spectrum
x_phase_sp = np.angle(fft_x)    # get audio phase spectrum

Visualizer.display_plots("Input audio", x, x_amplitude_sp, sr)

# load noise file, and stft (Short-time Fourier transform)
print('load wav', noisefile)
noise, noise_sr = librosa.load(noisefile, sr=None, mono=True)
fft_noise = librosa.stft(noise)
noise_amplitude_sp = np.abs(fft_noise)  # get audio amplitude spectrum
noise_footprint = np.mean(noise_amplitude_sp, axis=1) # get mean noise amplitude

Visualizer.display_plots("Noise audio", noise, noise_amplitude_sp, noise_sr)

# calculate output audio signal with istft (Inverse short-time Fourier transform)
y_amplitude_sp = (x_amplitude_sp - noise_footprint.reshape((noise_footprint.shape[0], 1))).clip(0.)  # reshape for broadcast to subtract
fft_y = y_amplitude_sp * np.exp(1.0j * x_phase_sp) # apply phase information
y = librosa.istft(fft_y) # back to time domain signal

Visualizer.display_plots("Output audio", y, y_amplitude_sp, sr)

# save as a wav file
scipy.io.wavfile.write(outfile, sr, (y * 32768).astype(np.int16))
print('write wav', outfile)
