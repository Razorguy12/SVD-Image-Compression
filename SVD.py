import cv2
import numpy as np
import matplotlib.pyplot as plt
import math
import qrcode

# 1. Load Image
image = cv2.imread('images.jpg')
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.imwrite('gray_image.jpeg', gray_image)
A = np.float64(gray_image)
m, n = A.shape

# 2. Compute SVD
U, S, Vt = np.linalg.svd(A, full_matrices=False)

# 3. Analyze Energy
total_energy = np.sum(S**2)

# 4. Determine k for 99.6% energy retention
target_energy = 0.996 * total_energy 

# print(f"Energy of first singular value alone: {(S[0]**2 / total_energy) * 100:.2f}%")

cumulative_energy = 0.0
k = 0

for singular_value in S:
    cumulative_energy += singular_value**2
    k += 1
    if cumulative_energy >= target_energy:
        break

print(f"Optimal k found for 99.5% energy: {k}")

# 5. Reconstruct Image with k singular values
U_k = U[:, :k]
S_k = np.diag(S[:k])
Vt_k = Vt[:k, :]

print(f"Shapes - U_k: {U_k.shape}, S_k: {S_k.shape}, Vt_k: {Vt_k.shape}")
A_k = U_k @ S_k @ Vt_k

print(f"Reconstructed image shape: {A_k.shape}")

# 6. Frobenius Norm Error
frobenius_error = np.linalg.norm(A - A_k, 'fro')
print(f"Frobenius norm of the error: {frobenius_error:.2f}")

# 7. Normalization
compressed_A = np.clip(A_k, 0, 255)
compressed_image = np.uint8(compressed_A)

cv2.imwrite('compressed_image.jpeg', compressed_image)
print("Compressed image saved as 'compressed_image.jpeg'")

# 8. Prepare payload (group SVD components and round to reduce size)
full_data = [
    np.round(U_k, 2).tolist(),
    np.round(S[:k], 2).tolist(),
    np.round(Vt_k, 2).tolist()
]

# 9. Serialize to text (convert structure to string for QR encoding)
payload_string = str(full_data)
total_chars = len(payload_string)

# 10. Determine QR chunk size (conservative limit ensures valid QR version)
QR_LIMIT = 2000
num_qrs = math.ceil(total_chars / QR_LIMIT)

print(f"Total Data Size: {total_chars} characters")
print(f"Splitting into {num_qrs} QR codes...")

# 11. Generate QR images (slice payload, prefix with order label, encode and save)
for i in range(num_qrs):
    start = i * QR_LIMIT
    end = start + QR_LIMIT
    chunk_data = payload_string[start:end]
    label = f"{i+1}/{num_qrs}:"
    final_content = label + chunk_data

    qr = qrcode.QRCode(
        version=None,
        box_size=10,
        border=4,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
    )
    qr.add_data(final_content)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    filename = f"qr_part_{i+1}.png"
    img.save(filename)
    print(f" -> Generated: {filename} (Contains chars {start} to {end})")

print("\nDONE: Generated QR parts for the compressed image payload.")

# 12. Visualize metrics (PSNR, energy retained, Frobenius error, compression ratio vs k)
# Sample k values to test and generate metric curves
k_test_values = list(range(1, min(m, n), max(1, (min(m, n) - 1) // 20)))
psnr_vals = []
energy_retained_vals = []
fro_error_vals = []
compression_ratio_vals = []

A_fro_norm = np.linalg.norm(A, 'fro')
total_energy_full = np.sum(S**2)
MAX_PIXEL = 255.0

for k_val in k_test_values:
    U_test = U[:, :k_val]
    S_test = np.diag(S[:k_val])
    Vt_test = Vt[:k_val, :]
    A_reconstructed = U_test @ S_test @ Vt_test

    # PSNR (Peak Signal-to-Noise Ratio)
    mse = np.mean((A - A_reconstructed)**2)
    if mse < 1e-10:
        psnr = 100.0
    else:
        psnr = 10 * np.log10((MAX_PIXEL**2) / mse)
    psnr_vals.append(psnr)

    # Energy retained (as percentage)
    energy_k = np.sum(S[:k_val]**2)
    energy_pct = (energy_k / total_energy_full) * 100
    energy_retained_vals.append(energy_pct)

    # Frobenius norm error
    fro_err = np.linalg.norm(A - A_reconstructed, 'fro')
    fro_error_vals.append(fro_err)

    # Compression ratio
    original_size = m * n
    compressed_size = k_val * (m + n + 1)
    cr = original_size / compressed_size
    compression_ratio_vals.append(cr)

# Create 2x2 subplots
plt.figure(figsize=(14, 10))

# Plot 1: PSNR vs k
plt.subplot(2, 2, 1)
plt.plot(k_test_values, psnr_vals, 'b-o', linewidth=2, markersize=6)
plt.axvline(x=k, color='r', linestyle='--', label=f'Optimal k={k}')
plt.title("PSNR vs Rank (k)", fontsize=12, fontweight='bold')
plt.xlabel("Rank (k)")
plt.ylabel("PSNR (dB)")
plt.grid(True, alpha=0.3)
plt.legend()

# Plot 2: Energy Retained vs k
plt.subplot(2, 2, 2)
plt.plot(k_test_values, energy_retained_vals, 'g-s', linewidth=2, markersize=6)
plt.axhline(y=99.6, color='r', linestyle='--', label='99.6% Target')
plt.axvline(x=k, color='r', linestyle='--', label=f'Optimal k={k}')
plt.title("Energy Retained vs Rank (k)", fontsize=12, fontweight='bold')
plt.xlabel("Rank (k)")
plt.ylabel("Energy Retained (%)")
plt.grid(True, alpha=0.3)
plt.legend()

# Plot 3: Frobenius Norm Error vs k
plt.subplot(2, 2, 3)
plt.plot(k_test_values, fro_error_vals, 'm-^', linewidth=2, markersize=6)
plt.axvline(x=k, color='r', linestyle='--', label=f'Optimal k={k}')
plt.title("Frobenius Norm Error vs Rank (k)", fontsize=12, fontweight='bold')
plt.xlabel("Rank (k)")
plt.ylabel("||A - A_k||_F")
plt.grid(True, alpha=0.3)
plt.legend()

# Plot 4: Compression Ratio vs k
plt.subplot(2, 2, 4)
plt.plot(k_test_values, compression_ratio_vals, 'c-d', linewidth=2, markersize=6)
plt.axvline(x=k, color='r', linestyle='--', label=f'Optimal k={k}')
plt.title("Compression Ratio vs Rank (k)", fontsize=12, fontweight='bold')
plt.xlabel("Rank (k)")
plt.ylabel("Compression Ratio")
plt.grid(True, alpha=0.3)
plt.legend()

plt.tight_layout()
plt.show()




