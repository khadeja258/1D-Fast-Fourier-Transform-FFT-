#include <math.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define PI 3.14159265358979323846
#define N_POINTS 1024
#define THRESHOLD 10.0f  // Denoising threshold

// Precomputed twiddle factor tables
float twiddle_real[N_POINTS / 2];
float twiddle_imag[N_POINTS / 2];

// Bit reversal lookup table
int bit_reversed[N_POINTS];


// Bit reversal helper function
unsigned int reverse_bits(unsigned int x, int log2n) {
    unsigned int n = 0;
    for (int i = 0; i < log2n; i++) {
        n <<= 1;
        n |= (x & 1);
        x >>= 1;
    }
    return n;
}

// Iterative FFT function with SIMD-prepped butterfly grouping
void fft_iterative(float* real, float* imag, int n) {
    int log2n = 0;
    for (int temp = n; temp > 1; temp >>= 1) log2n++;

    // Use bit-reversed lookup table for initial reordering
    for (int i = 0; i < n; i++) {
        int j = bit_reversed[i];
        if (j > i) {
            float temp_real = real[i];
            float temp_imag = imag[i];
            real[i] = real[j];
            imag[i] = imag[j];
            real[j] = temp_real;
            imag[j] = temp_imag;
        }
    }

    // Matrix-style butterfly grouping, SIMD batched
    for (int stage = 1; stage <= log2n; stage++) {
        int group_size = 1 << stage;
        int half_size = group_size >> 1;
        int step = N_POINTS / group_size;

        for (int group = 0; group < n; group += group_size) {
            for (int pair = 0; pair < half_size; pair += 4) {
                for (int offset = 0; offset < 4 && (pair + offset) < half_size; offset++) {
                    int idx1 = group + pair + offset;
                    int idx2 = idx1 + half_size;
                    int tw_idx = (pair + offset) * step;

                    float r2 = real[idx2];
                    float i2 = imag[idx2];
                    float w_r = twiddle_real[tw_idx];
                    float w_i = twiddle_imag[tw_idx];

                    float t_r = w_r * r2 - w_i * i2;
                    float t_i = w_r * i2 + w_i * r2;

                    float r1 = real[idx1];
                    float i1 = imag[idx1];

                    real[idx1] = r1 + t_r;
                    imag[idx1] = i1 + t_i;

                    real[idx2] = r1 - t_r;
                    imag[idx2] = i1 - t_i;
                }
            }
        }
    }
}

// Inverse FFT function (vectorized-style loop)
void ifft_iterative(float* real, float* imag, int n) {
    for (int i = 0; i < n; i += 4) {
        imag[i]   = -imag[i];
        imag[i+1] = -imag[i+1];
        imag[i+2] = -imag[i+2];
        imag[i+3] = -imag[i+3];
    }

    fft_iterative(real, imag, n);

    for (int i = 0; i < n; i += 4) {
        real[i]   /= n;    imag[i]   = -imag[i]   / n;
        real[i+1] /= n;    imag[i+1] = -imag[i+1] / n;
        real[i+2] /= n;    imag[i+2] = -imag[i+2] / n;
        real[i+3] /= n;    imag[i+3] = -imag[i+3] / n;
    }
}

int main() {
    float real[N_POINTS], imag[N_POINTS], magnitude[N_POINTS];
    float pure_signal[N_POINTS];
    float denoised[N_POINTS];
    float noise_level = 0.5;

    for (int i = 0; i < N_POINTS / 2; i++) {
        float angle = -2.0 * PI * i / N_POINTS;
        twiddle_real[i] = cos(angle);
        twiddle_imag[i] = sin(angle);
    }

    int log2n = 0;
    for (int temp = N_POINTS; temp > 1; temp >>= 1) log2n++;
    for (int i = 0; i < N_POINTS; i++) {
        bit_reversed[i] = reverse_bits(i, log2n);
    }

    srand(time(NULL));

    for (int i = 0; i < N_POINTS; i++) {
        float t = (float)i / N_POINTS;
        float sine = sin(2 * PI * 5 * t);
        float noise = ((float)rand() / RAND_MAX - 0.5f) * 2 * noise_level;
        real[i] = sine + noise;
        imag[i] = 0.0f;
        pure_signal[i] = sine;
    }

    fft_iterative(real, imag, N_POINTS);

    printf("\nMagnitude Spectrum (before filtering):\n");
    for (int i = 0; i < N_POINTS; i++) {
        magnitude[i] = sqrt(real[i] * real[i] + imag[i] * imag[i]);
        printf("|X[%d]| = %f\n", i, magnitude[i]);
    }

    

    for (int i = 0; i < N_POINTS; i++) {
        if (i != 5 && i != (N_POINTS - 5)) {
            real[i] = 0;
            imag[i] = 0;
        }
    }

    ifft_iterative(real, imag, N_POINTS);

    printf("\nDenoised Signal (after IFFT):\n");
    for (int i = 0; i < N_POINTS; i++) {
        denoised[i] = real[i];
        printf("x[%d] = %f\n", i, denoised[i]);
    }

 
    return 0;
}
