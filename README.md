# 1D-Fast-Fourier-Transform-FFT-
 This project was made as part of our Computer Architecture and Assembly Language course. 
 It focuses on implementing the Fast Fourier Transform (FFT) and its inverse (IFFT), which is an efficient algorithm to compute the Discrete Fourier Transform (DFT) of a sequence. The FFT transforms a signal from the time domain to the frequency domain, allowing us to analyze its frequency components so instead of directly computing the DFT which has a time complexity of O(n²) the FFT reduces it to O(n log n) by breaking the problem into smaller parts and using the symmetries of complex exponentials.

# Implementation
The FFT logic was adapted by watching various YouTube tutorials. Based on those, we wrote a C program, which makes it relatively easier to translate into assembly language, which can be run on Veer Simulator on Ubuntu, while a Python program was made to plot the graphs.


# Code Structure
- fft_riscv.c -> Iterative FFT/IFFT in C with SIMD-friendly structure, twiddle factor optimization, bit-reversal, and denoising for RISC-V assembly/vectorization.
- ft final 1.c ->  adds noise to a sine wave, uses FFT to move to frequency domain, filters out noise, then uses IFFT to recover a clean signal.
- fft.py -> Generates a noisy sine wave, applies a recursive FFT to analyze its frequency content, and plots the signals and their spectrum.
- plotting.py -> Visualizes the FFT magnitude spectrum, compares pure vs noisy sine wave, and shows the denoised signal obtained using FFT filtering and IFFT.
- twiddle_comp.py -> Generates and prints cosine and negative sine values for 1024-point FFT twiddle factors in RISC-V assembly .float format.
- to_float.py -> Converts a hex string of 32-bit floats into a reversed list of rounded float values.
- vectorized.s -> RISC-V vectorized FFT implementation performing bit-reversal ordering, iterative butterfly computations, and printing results, with both forward and inverse FFT support.






 
