import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import convolve

# -------------------------------
# 1. Model Setup
# -------------------------------
nx = 100      # Number of horizontal traces
nz = 200      # Number of vertical/depth samples
n_layers = 10 # Number of layers
dt = 0.001    # Sampling interval (s)
wavelet_length = 0.128  # Length of Ricker wavelet in seconds

# -------------------------------
# 2. Generate Random Velocities and Densities Per Layer
# -------------------------------
np.random.seed(42)  # For reproducibility

layer_thickness = nz // n_layers
vel_model = np.zeros((nz, nx))
rho_model = np.zeros((nz, nx))

# Assign a random velocity and density to each layer
velocities = np.random.uniform(1500, 3000, n_layers)
densities = np.random.uniform(1800, 2600, n_layers)

for i in range(n_layers):
    start = i * layer_thickness
    end = (i + 1) * layer_thickness
    vel_model[start:end, :] = velocities[i]
    rho_model[start:end, :] = densities[i]

# -------------------------------
# 3. Compute Reflection Coefficients (Vertical Only)
# -------------------------------
R_model = np.zeros_like(vel_model)

for i in range(nz - 1):
    rho1 = rho_model[i, :]
    rho2 = rho_model[i + 1, :]
    v1 = vel_model[i, :]
    v2 = vel_model[i + 1, :]

    Z1 = rho1 * v1
    Z2 = rho2 * v2
    R_model[i, :] = (Z2 - Z1) / (Z2 + Z1)

# -------------------------------
# 4. Ricker Wavelet Generator
# -------------------------------
def ricker_wavelet(frequency, dt, length):
    t = np.arange(-length / 2, length / 2, dt)
    y = (1 - 2 * (np.pi**2) * (frequency**2) * (t**2)) * \
        np.exp(-(np.pi**2) * (frequency**2) * (t**2))
    return y

# Generate wavelet
fc = 25  # Central frequency in Hz
wavelet = ricker_wavelet(fc, dt, wavelet_length)

# -------------------------------
# 5. Convolve and Add Gaussian Noise
# -------------------------------
seismic = np.zeros_like(R_model)

for ix in range(nx):
    trace = convolve(R_model[:, ix], wavelet, mode='same')
    
    # Add Gaussian noise
    noise = np.random.normal(0, 0.05, size=trace.shape)
    seismic[:, ix] = trace + noise

# -------------------------------
# 6. Display the Seismic Image
# -------------------------------
__import__('pdb').set_trace()
plt.figure(figsize=(12, 6))
plt.imshow(seismic, cmap='gray', aspect='auto', extent=[0, nx, nz * dt, 0])
plt.title("Seismic Image: 10-Layer Model with Variable Properties + Noise")
plt.xlabel("Trace Number")
plt.ylabel("Time (s)")
plt.colorbar(label="Amplitude")
plt.tight_layout()
plt.show()
