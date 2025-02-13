import numpy as np

M = 16
log2M = int(np.log2(M))
qam_symbols = np.array([(2 * (i % np.sqrt(M)) - np.sqrt(M) + 1) + 
                             1j * (2 * (i // np.sqrt(M)) - np.sqrt(M) + 1) 
                             for i in range(M)])
qam_map = {format(i, f'0{log2M}b'): qam_symbols[i] for i in range(M)}
qam_demod_map = {v: k for k, v in qam_map.items()}

def bits_to_qam(bits):
    bit_strings = ["".join(map(str, b)) for b in bits.reshape(-1, log2M)]
    symbols = np.array([qam_map[b] for b in bit_strings])
    return symbols

def str_to_binary(string):
	# Initialize empty list to store binary values
	binary_list = []
	
	# Iterate through each character in the string
	for char in string:
		# Convert character to binary, pad with leading zeroes and append to list
		binary_list.append(bin(ord(char))[2:].zfill(8))
		
	# Join the binary values in the list and return as a single string
	return ''.join(binary_list)


input = 'helloasdfasdf'
bits = np.array([0,0,0,1,1,1,1,1])
bits_string = np.array([i for i in str_to_binary(input)])
print(bits_to_qam(bits_string))


# bits_to_qam() take k*log2M bits in the array format (np.array) as input and return an array of complex symbol

# str_to_binary() turn a string to a binary sequence 
# --> need to use np.array to reformat the sequence to be an array