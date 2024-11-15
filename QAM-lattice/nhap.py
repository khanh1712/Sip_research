import numpy as np
from numpy.linalg import det, norm

def hadamard_ratio(basis):
    """Calculate the Hadamard ratio of a lattice basis."""
    n = basis.shape[0]
    det_basis = abs(det(basis))
    norms_product = np.prod([norm(vec) for vec in basis])
    return det_basis / norms_product

def gram_schmidt(basis):
    """Apply Gram-Schmidt orthogonalization to improve the basis orthogonality."""
    n = basis.shape[0]
    ortho_basis = np.zeros_like(basis, dtype=float)
    for i in range(n):
        vec = basis[i]
        for j in range(i):
            proj = np.dot(ortho_basis[j], vec) / np.dot(ortho_basis[j], ortho_basis[j])
            vec = vec - proj * ortho_basis[j]
        ortho_basis[i] = vec
    return np.round(ortho_basis).astype(int)

def generate_good_basis(n, min_hadamard=0.8):
    """Generate a good basis with Hadamard ratio ≥ min_hadamard."""
    while True:
        basis = np.random.randint(-10, 10, size=(n, n))  # Step 1.1: Generate random basis
        if abs(det(basis)) > 0:  # Ensure basis is full-rank
            basis = gram_schmidt(basis)  # Step 1.2: Apply Gram-Schmidt
            ratio = hadamard_ratio(basis)
            if ratio >= min_hadamard:
                return basis

def generate_bad_basis(good_basis, max_hadamard=0.001):
    """Generate a bad basis with Hadamard ratio ≤ max_hadamard."""
    n = good_basis.shape[0]
    while True:
        unimodular = np.random.randint(-10, 10, size=(n, n))
        if abs(det(unimodular)) == 1:  # Ensure unimodular property
            bad_basis = np.dot(good_basis, unimodular)
            ratio = hadamard_ratio(bad_basis)
            if ratio <= max_hadamard:
                return bad_basis

# Example Usage
n = 16  # Lattice dimension
private_key = generate_good_basis(n)
public_key = generate_bad_basis(private_key)

print("Private Key (Good Basis):")
print(private_key)
print("Private Key Hadamard Ratio:", hadamard_ratio(private_key))

print("\nPublic Key (Bad Basis):")
print(public_key)
print("Public Key Hadamard Ratio:", hadamard_ratio(public_key))
