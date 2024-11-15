import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import LKG

def initialize_parameters(p, N):
    """
    Initializes parameters for QAM modulation and matrix multiplication.
    """
    M = 2 ** p  # QAM-M
    return M, N

def image_to_bitstream(image_path):
    """
    Converts an image to a binary bitstream.
    """
    img = Image.open(image_path).convert('L')  # Convert to grayscale
    img = img.resize((512, 512))  # Resize for manageability
    img_array = np.array(img)  # Convert image to numpy array
    img_flat = img_array.flatten()  # Flatten the array
    bitstream = np.unpackbits(img_flat)  # Convert pixels to binary bitstream
    return bitstream, img_array.shape

def bits_to_qam_symbols(bit_group, p):
    """
    Maps a group of `p * N` bits to QAM symbols and outputs an N*1 matrix.
    """
    M = 2 ** p
    qam_levels = int(np.sqrt(M))
    constellation = np.array([complex(i, j) for i in range(-qam_levels + 1, qam_levels, 2)
                              for j in range(-qam_levels + 1, qam_levels, 2)])
    
    # Group the bitstream into chunks of `p` bits for each QAM symbol
    num_symbols = len(bit_group) // p
    bit_groups = bit_group.reshape(num_symbols, p)
    
    # Convert each group of p bits to an integer and map to constellation point
    indices = bit_groups.dot(2 ** np.arange(p)[::-1])
    A = constellation[indices]
    return A.reshape(num_symbols, 1)

def multiply_with_matrix(A, matrix_N):
    """
    Multiplies an N*1 matrix A with an N*N matrix.
    """
    return np.dot(matrix_N, A)

def add_gaussian_noise(B, snr_db):
    """
    Adds Gaussian noise to the signal B based on the given SNR (in dB).
    """
    signal_power = np.mean(np.abs(B) ** 2)
    snr_linear = 10 ** (snr_db / 10)
    noise_power = signal_power / snr_linear
    noise = np.sqrt(noise_power / 2) * (np.random.randn(*B.shape) + 1j * np.random.randn(*B.shape))
    C = B + noise
    return C

def demodulate_qam_symbols(C, p, constellation):
    """
    Demodulates noisy QAM symbols back to bits.
    """
    distances = abs(C.reshape(-1, 1) - constellation.reshape(1, -1))
    closest_symbols = distances.argmin(axis=1)
    
    bits_per_symbol = int(np.log2(len(constellation)))
    bitstream = np.array([(np.binary_repr(i, bits_per_symbol)) for i in closest_symbols])
    bitstream = np.array([int(bit) for bit in ''.join(bitstream)])
    return bitstream

def bitstream_to_image(bits, image_shape):
    """
    Converts a binary bitstream back into an image.
    """
    pixels = np.packbits(bits)  # Convert binary stream to pixel values
    img_array = pixels[:image_shape[0] * image_shape[1]].reshape(image_shape)  # Reshape to original dimensions
    return Image.fromarray(img_array)

def plot_matrices(A, B, C):
    """
    Plots the matrices A, B, and C in the complex plane.
    """
    plt.figure(figsize=(15, 5))
    
    plt.subplot(1, 3, 1)
    plt.scatter(np.real(A), np.imag(A), color='blue')
    plt.title("Matrix A (Original Symbols)")
    plt.xlabel("In-phase")
    plt.ylabel("Quadrature")
    plt.grid(True)
    plt.axis('equal')
    
    plt.subplot(1, 3, 2)
    plt.scatter(np.real(B), np.imag(B), color='green')
    plt.title("Matrix B (After Matrix Multiplication)")
    plt.xlabel("In-phase")
    plt.ylabel("Quadrature")
    plt.grid(True)
    plt.axis('equal')
    
    plt.subplot(1, 3, 3)
    plt.scatter(np.real(C), np.imag(C), color='red')
    plt.title("Matrix C (Received with Noise)")
    plt.xlabel("In-phase")
    plt.ylabel("Quadrature")
    plt.grid(True)
    plt.axis('equal')
    
    plt.show()

# Parameters
p = 4          # Number of bits per QAM symbol
N = 256         # Size of the encryption matrix (N x N)
snr_db = 20    # Signal-to-noise ratio in dB
image_path = 'C:/Users/ADMIN/.vscode/khanh/Lab demo/QAM-lattice/Lenna_(test_image).jpg'  # Replace with the path to your image

# Step 0: Initialize parameters
M, N = initialize_parameters(p, N)

# Step 1: Convert the image to a bitstream
bitstream, image_shape = image_to_bitstream(image_path)

# Step 2-4: Process each block of p*N bits through QAM and noisy channel
num_bits_per_block = p * N
num_blocks = len(bitstream) // num_bits_per_block

received_bitstream = np.array([], dtype=int)
constellation = np.array([complex(i, j) for i in range(-3, 4, 2) for j in range(-3, 4, 2)])

# encryption_matrix = np.random.randn(N, N) + 1j * np.random.randn(N, N)  # Random complex matrix
encryption_matrix, decryption_matrix = LKG.generate_key_pair(N)
print(encryption_matrix)

for i in range(num_blocks):
    # Extract p*N bits for the current block
    bit_block = bitstream[i * num_bits_per_block : (i + 1) * num_bits_per_block]
    
    # Step 2: Map bits to QAM symbols to form matrix A
    A = bits_to_qam_symbols(bit_block, p)
    
    # Step 3: Multiply A with an N*N encryption matrix
    
    B = multiply_with_matrix(A, encryption_matrix)
    
    # Step 4: Add Gaussian noise to simulate transmission through a noisy channel
    C = add_gaussian_noise(B, snr_db)
    
    # Plot matrices for the first block to observe the changes
    if i == 0:
        plot_matrices(A, B, C)
    
    # Step 6: Demodulate matrix C to obtain received bits for this block
    received_bits_block = demodulate_qam_symbols(C, p, constellation)
    received_bitstream = np.concatenate((received_bitstream, received_bits_block))

# Step 7: Convert the received bitstream back to an image
received_image = bitstream_to_image(received_bitstream, image_shape)

# Display the original and received images
original_image = Image.open(image_path).convert('L').resize((512, 512))
plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
plt.imshow(original_image, cmap='gray')
plt.title("Original Image")
plt.axis('off')

plt.subplot(1, 2, 2)
plt.imshow(received_image, cmap='gray')
plt.title(f"Received Image (SNR = {snr_db} dB)")
plt.axis('off')
plt.show()
