import numpy as np
import time
import matplotlib.pyplot as plt
from cmath import exp, pi

def FFT(f):
    N = len(f)
    if N <= 1:
        return f

    even = FFT(f[0::2])
    odd = FFT(f[1::2])

    temp = np.zeros(N, dtype=np.complex64)

    for u in range(N//2):
        temp[u] = even[u] + exp(-2j*pi*u/N) * odd[u]
        temp[u+N//2] = even[u] - exp(-2j*pi*u/N) * odd[u]

    return temp

 # ----------- Create Sine Wave and Add Noise -----------
N = 1024  # Length of signal
t = np.linspace(0, 1, N, endpoint=False)  # Time vector

# Pure sine wave (Frequency = 5 Hz)
freq = 5  # 5 Hz
pure_signal = np.sin(2 * np.pi * freq * t)

# Add small random noise
noise = 0.5 * np.random.normal(0, 1, N)  # Random noise scaled by 0.5
noisy_signal = pure_signal + noise

# ----------- Apply FFT to Noisy Signal -----------
F_noisy = FFT(noisy_signal)

# Compute frequency axis for plotting
frequencies = np.fft.fftfreq(N, d=(t[1] - t[0]))


# ----------- Plot Results -----------
plt.figure(figsize=(14, 6))

# Plot the pure and noisy signals
plt.subplot(2,1,1)
plt.plot(t, pure_signal, label='Pure Sine Wave')
plt.plot(t, noisy_signal, label='Noisy Signal', alpha=0.6)
plt.title('Pure vs Noisy Signal')
plt.legend()

# Plot the magnitude spectrum
plt.subplot(2,1,2)
plt.plot(frequencies[:N//2], np.abs(F_noisy)[:N//2])
plt.title('FFT of Noisy Signal')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Amplitude')
plt.grid(True)

plt.tight_layout()
plt.show()