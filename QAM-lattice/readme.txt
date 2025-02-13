THIS IS DOCUMENTED BY KHANH1712

* files notes
1. ver1.py: original version with 1 value (N, M)
2. ver2.py: multiple N, 1 M
3. ver3.py: multiple (N, M)
4. ver4.py: compare with theoretical BER

* function notes
1. N is the number of subcarriers. M is the QAM level
2. bits_to_qam() take k*log2M bits in the array format (np.array) as input and return an array of complex symbol

3. str_to_binary() turn a string to a binary sequence 
--> need to use np.array to reformat the sequence to be an array

*Execution notes
1. Each value pair (N, M) takes about 90 secs for 10^6 bits input