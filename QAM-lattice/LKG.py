import numpy as np

def generate_unimodular_matrix(n):
    # Start with an identity matrix
    U = np.eye(n, dtype=int)
    # Apply random row and column operations to make it unimodular
    for i in range(n):
        for j in range(i + 1, n):
            U[i, j] += np.random.randint(-5, 5)
            U[j, i] += np.random.randint(-5, 5)
    return U

def generate_key_pair(n):
    # Step 1: Generate a good basis B (private key)
    B = np.random.randint(-10, 10, (n, n))
    
    # Ensure B is invertible
    while np.linalg.det(B) == 0:
        B = np.random.randint(-10, 10, (n, n))

    # Step 2: Generate a random unimodular matrix U
    U = generate_unimodular_matrix(n)

    # Step 3: Compute the public basis B' = B * U
    B_public = np.dot(B, U)
    
    return B, B_public

# Example usage
n = 256  # Dimension of the lattice
private_key, public_key = generate_key_pair(n)

print("Private Key (Good Basis):\n", private_key)
print("Public Key (Bad Basis):\n", public_key)
