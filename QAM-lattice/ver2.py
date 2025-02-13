# multiple value of N

import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, ifft
from time import time
# Simulation Parameters
N_values = [16, 32, 64, 128]  # Different values of N
M = 16  # QAM Modulation order (16-QAM)
log2M = int(np.log2(M))
num_bits = 10**7
SNR_dB = np.arange(0, 31, 2.5)  # SNR range in dB

# QAM Symbol Mapping
qam_symbols = np.array([-3-3j, -3-1j, -3+3j, -3+1j, 
                         -1-3j, -1-1j, -1+3j, -1+1j, 
                          3-3j,  3-1j,  3+3j,  3+1j, 
                          1-3j,  1-1j,  1+3j,  1+1j])
qam_map = {format(i, f'0{log2M}b'): qam_symbols[i] for i in range(M)}
qam_demod_map = {v: k for k, v in qam_map.items()}

# Function to map bits to QAM symbols
def bits_to_qam(bits):
    bit_strings = ["".join(map(str, b)) for b in bits.reshape(-1, log2M)]
    symbols = np.array([qam_map[b] for b in bit_strings])
    return symbols

# Function to demap QAM symbols back to bits
def qam_to_bits(symbols):
    demapped_bits = np.array([list(qam_demod_map[min(qam_symbols, key=lambda x: abs(x - s))]) for s in symbols])
    return demapped_bits.astype(int).flatten()

plt.figure(figsize=(8, 6))

start = time()
for N in N_values:
    num_blocks = num_bits // (N * log2M)
    ber = []
    
    for snr in SNR_dB:
        errors = 0
        noise_var = 10**(-snr / 10) / log2M
        
        for _ in range(num_blocks):
            bits = np.random.randint(0, 2, (N * log2M))  # Step 1: Bit Generation
            qam_symbols = bits_to_qam(bits)  # Step 3: QAM Mapping
            ofdm_symbols = ifft(qam_symbols)  # Step 4: IFFT
            noise = np.sqrt(noise_var / 2) * (np.random.randn(N) + 1j * np.random.randn(N))
            received = ofdm_symbols + noise  # Step 5: AWGN Channel
            received_qam = fft(received)  # Step 6: FFT
            received_bits = qam_to_bits(received_qam)  # Step 7: QAM Demapping
            errors += np.sum(bits != received_bits)
            
        ber.append(errors / num_bits)
        print(ber)
    plt.semilogy(SNR_dB, ber, 'o-', label=f'N={N}')

end = time()
print("Duration: ", end - start)
plt.xlabel('SNR (dB)')
plt.ylabel('Bit Error Rate (BER)')
plt.title('SNR vs BER for QAM-OFDM System with Different N')
plt.grid(True, which='both', linestyle='--')
plt.legend()
plt.show()
