# 🧠 SVD Image Compression and QR Encoding

This project implements image compression using **Singular Value Decomposition (SVD)** and stores the compressed image data as **multiple QR codes**.

The system converts an image into a matrix, performs SVD decomposition, selects an optimal rank that retains **99.6% of the image energy**, reconstructs the image, evaluates compression quality, and encodes the compressed data into QR codes.

This project demonstrates how **linear algebra techniques can be applied to image compression and efficient data storage.**

------------------------------------------------------------

## 📚 Singular Value Decomposition (SVD)

Singular Value Decomposition is a matrix factorization technique used in linear algebra.

Any matrix A can be decomposed as:

A = U Σ Vᵀ

Where:

A = Original image matrix (m × n)  
U = Left singular vectors  
Σ = Diagonal matrix of singular values  
Vᵀ = Right singular vectors  

The singular values represent the importance of different components of the image.

Larger singular values contain most of the image information.

By keeping only the largest k singular values, the image can be compressed while maintaining quality.

------------------------------------------------------------

## 🎯 Project Goals

• Compress an image using SVD  
• Retain 99.6% of image energy  
• Reconstruct the compressed image  
• Measure reconstruction quality  
• Calculate compression metrics  
• Store compressed data in QR codes  
• Visualize performance metrics

------------------------------------------------------------

## 📁 Project Structure

svd-image-compression/

README.md  
main.py  
images.jpeg  
gray_image.jpeg  
compressed_image.jpeg  
qr_part_1.png  
qr_part_2.png  
...

------------------------------------------------------------

## ⚙️ Algorithm Steps

### 1. Load Image

The image is loaded using OpenCV and converted into grayscale.

Input file:

images.jpeg

Grayscale output:

gray_image.jpeg

Grayscale images simplify processing and reduce computation.

------------------------------------------------------------

### 2. Matrix Representation

The grayscale image is converted into a matrix A of size:

m × n

The matrix is converted to floating point format for accurate calculations.

------------------------------------------------------------

### 3. Singular Value Decomposition

The image matrix is decomposed:

A = U Σ Vᵀ

Using:

U, S, Vt = np.linalg.svd(A, full_matrices=False)

Where:

U = Left singular vectors  
S = Singular values  
Vt = Right singular vectors

------------------------------------------------------------

### 4. Energy Analysis

Image energy is defined as:

Energy = sum of (singular value²)

Total energy is computed as:

total_energy = Σ S²

The algorithm selects the minimum k such that:

Energy retained ≥ 99.6%

This ensures high visual quality with reduced storage.

------------------------------------------------------------

### 5. Optimal Rank Selection

The smallest k satisfying:

cumulative_energy ≥ 0.996 × total_energy

is selected automatically.

Example output:

Optimal k found for 99.6% energy: 35

------------------------------------------------------------

## 📉 Image Compression

Instead of storing the full matrix A, only the first k components are stored:

U_k  
Σ_k  
V_kᵀ

Reconstruction:

A_k = U_k Σ_k V_kᵀ

This significantly reduces storage requirements.

------------------------------------------------------------

## 📏 Error Measurement

### Frobenius Norm Error

Measures reconstruction accuracy:

||A − A_k||_F

Computed using:

np.linalg.norm(A - A_k, 'fro')

Lower values indicate better reconstruction.

------------------------------------------------------------

### PSNR (Peak Signal-to-Noise Ratio)

Measures visual quality of the reconstructed image.

PSNR = 10 log10(MAX² / MSE)

Where:

MAX = 255  
MSE = Mean Squared Error

Higher PSNR indicates better image quality.

------------------------------------------------------------

## 📊 Compression Ratio

Original size:

m × n

Compressed size:

k × (m + n + 1)

Compression Ratio:

Compression Ratio = Original Size / Compressed Size

Higher compression ratio means better compression.

------------------------------------------------------------

## 🧾 Image Reconstruction

The compressed image is reconstructed using:

A_k = U_k Σ_k V_kᵀ

The image values are normalized to the range:

0 – 255

Output file:

compressed_image.jpeg

------------------------------------------------------------

## 📦 QR Code Encoding

The compressed SVD components are stored:

• U_k matrix  
• Singular values S_k  
• V_kᵀ matrix

Values are rounded to reduce size.

Example:

np.round(U_k, 2)

The data is converted into a text string.

Since QR codes have size limits, the data is split into multiple parts.

Each QR code contains a labeled segment:

1/5:data...  
2/5:data...

Generated files:

qr_part_1.png  
qr_part_2.png  
qr_part_3.png  
...

------------------------------------------------------------

## 📊 Visualization Metrics

The program generates four plots.

------------------------------------------------------------

### 1. PSNR vs Rank

Shows image quality as rank increases.

Higher rank produces better image quality.

------------------------------------------------------------

### 2. Energy Retained vs Rank

Shows percentage of information preserved.

Target energy retention:

99.6%

------------------------------------------------------------

### 3. Frobenius Error vs Rank

Shows reconstruction error.

Lower error indicates better reconstruction.

------------------------------------------------------------

### 4. Compression Ratio vs Rank

Shows storage efficiency.

Lower rank results in higher compression.

------------------------------------------------------------

## ▶️ How to Run

Install dependencies:

pip install numpy opencv-python matplotlib qrcode pillow

Run the program:

python main.py

------------------------------------------------------------

## 📥 Input

Place the input image:

images.jpeg

inside the project folder.

------------------------------------------------------------

## 📤 Output Files

The program generates:

gray_image.jpeg

compressed_image.jpeg

qr_part_*.png

Performance metric plots

------------------------------------------------------------

## 🧪 Example Output

Optimal k found for 99.6% energy: 35

Frobenius norm of the error: 142.32

Total Data Size: 9500 characters

Splitting into 5 QR codes...

DONE: Generated QR parts for the compressed image payload.

------------------------------------------------------------

## 🔧 Technologies Used

Python  
NumPy  
OpenCV  
Matplotlib  
QRCode Library

------------------------------------------------------------
	
Add files via upload
	
Feb 26, 2026
qr_part_11.png
	
Add files via upload
	
Feb 26, 2026
qr_part_12.png
	
Add files via upload
	
Feb 26, 2026
qr_part_13.png
## 🎯 Applications

Image compression  
Low-bandwidth image transmission  
QR-based data storage  
Edge computing  
Educational demonstrations

------------------------------------------------------------

## 🔮 Future Improvements

QR decoding and automatic reconstruction

Color image compression

Graphical interface

Cloud storage integration

------------------------------------------------------------

## 👨‍💻 Author

Mohammed Azhar Sait H
Satyajit S
Sai Akshay

