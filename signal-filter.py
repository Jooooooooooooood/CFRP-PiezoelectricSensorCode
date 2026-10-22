from scipy.signal import butter, sosfiltfilt, detrend
from scipy.stats import kurtosis

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Adapt that I can take a folder and pull all the files from it and filter them, saved as new files with all my important
# datapoints included (in a clean way)
fileName = input("File Name: ") ######
signalFile = open(fileName + ".csv")
raw_data = signalFile.read()
signalFile.close()

raw_signal = raw_data(1)
raw_time = raw_data(0)

fs = 1000       # Sampling frequency: 1000 Hz
cutoff = 100    # Cutoff frequency: 100 Hz
order = 4

sos = butter(
    order,
    cutoff,
    btype="lowpass",
    fs=fs,
    output="sos"
)

filtered_signal = sosfiltfilt(sos, raw_signal)
filtered_data = [raw_time, filtered_signal]

fig, ax = plt.subplots(2, 1, figsize=(10, 6), sharex=True)

# Raw signal
ax[0].plot(raw_time, raw_signal)
ax[0].set_title("Raw Signal")
ax[0].set_ylabel("Amplitude")
ax[0].grid(True)

# Filtered signal
ax[1].plot(raw_time, filtered_signal)
ax[1].set_title("Filtered Signal")
ax[1].set_xlabel("Time (s)")
ax[1].set_ylabel("Amplitude")
ax[1].grid(True)

plt.tight_layout()
plt.show()

data = extract_features(filtered_signal, fs)

filteredSignalFile = open(fileName + "_filtered.csv")
filteredSignalFile.write(filtered_signal)
filteredSignalFile.write(data)
filteredSignalFile.close()

def extract_features(x, fs):
    """Calculate time-domain and frequency-domain features."""
    x = np.asarray(x, dtype=float)
    n = len(x)

    # Time-domain features
    rms = np.sqrt(np.mean(x**2))
    peak = np.max(np.abs(x))
    energy = np.sum(x**2) / fs

    # Excess kurtosis: Gaussian noise has expected value near zero.
    kurt = kurtosis(x, fisher=True, bias=False)

    # Frequency-domain features
    window = np.hanning(n)
    spectrum = np.abs(np.fft.rfft(x * window))**2
    frequencies = np.fft.rfftfreq(n, d=1/fs)

    # Ignore DC when identifying the dominant frequency.
    if len(spectrum) > 1:
        dominant_idx = 1 + np.argmax(spectrum[1:])
        dominant_freq = frequencies[dominant_idx]
    else:
        dominant_freq = 0.0

    spectral_power = spectrum[1:]
    spectral_freqs = frequencies[1:]
    total_power = np.sum(spectral_power)

    spectral_centroid = (
        np.sum(spectral_freqs * spectral_power) / total_power
        if total_power > 0 else 0.0
    )

    return {
        "rms": rms,
        "peak_amplitude": peak,
        "kurtosis": kurt,
        "energy": energy,
        "dominant_frequency_hz": dominant_freq,
        "spectral_centroid_hz": spectral_centroid,
    }