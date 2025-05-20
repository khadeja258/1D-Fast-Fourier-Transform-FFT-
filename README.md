# 1D-Fast-Fourier-Transform-FFT-
 This project was made as part of our Computer Architecture and Assembly Language course. 
 It focuses on implementing the Fast Fourier Transform (FFT) and its inverse (IFFT), which is an efficient algorithm to compute the Discrete Fourier Transform (DFT) of a sequence. The FFT transforms a signal from the time domain to the frequency domain, allowing us to analyze its frequency components so instead of directly computing the DFT which has a time complexity of O(n²) the FFT reduces it to O(n log n) by breaking the problem into smaller parts and using the symmetries of complex exponentials.

# Implementation
The FFT logic was adapted by watching various YouTube tutorials. Based on those, we wrote a C program, which makes it relatively easier to translate into assembly language, which can be run on Veer Simulator on Ubuntu, while a Python program was made to plot the graphs.


# Code Structure




 
