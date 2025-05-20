import math

N = 1024
print('.section .rodata\n.align 6\nW_real_max:')
for k in range(N // 2):
    if k % 4 == 0:
        print('    .float ', end='')
    print(f'{math.cos(2 * math.pi * k / N):.9e},', end='\n' if k % 4 == 3 else ' ')
print('\n.align 6\nW_imag_max:')
for k in range(N // 2):
    if k % 4 == 0:
        print('    .float ', end='')
    print(f'{-math.sin(2 * math.pi * k / N):.9e},', end='\n' if k % 4 == 3 else ' ')