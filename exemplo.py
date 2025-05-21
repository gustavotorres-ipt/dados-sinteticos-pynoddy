import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import convolve

# Helper function to generate a Ricker wavelet
def ricker_wavelet(f, dt, t_max):
    t = np.arange(-t_max, t_max, dt)  # Time vector centered at 0
    return (1 - 2 * np.pi ** 2 * f ** 2 * t ** 2) * np.exp(-np.pi ** 2 * f ** 2 * t ** 2)

# Parameters
num_layers = 5
num_interfaces = num_layers - 1
num_samples = 500  # Number of time samples
dt = 0.002  # Time step (2 ms sample rate)
t_max = 0.1  # Maximum time for wavelet (100 ms)
f_min, f_max = 10, 60  # Frequency range for random sampling

# Define properties for each layer: [density, velocity]
properties = np.array([
    [2.0, 1500],  # Layer 1 (rho=2.0 g/cm³, V=1500 m/s)
    [2.3, 1700],  # Layer 2 (rho=2.3 g/cm³, V=1700 m/s)
    [2.5, 2000],  # Layer 3 (rho=2.5 g/cm³, V=2000 m/s)
    [2.4, 2200],  # Layer 4 (rho=2.4 g/cm³, V=2200 m/s)
    [2.6, 2500],  # Layer 5 (rho=2.6 g/cm³, V=2500 m/s)
])

# Calculate reflection coefficients
reflection_coefficients = np.zeros((num_interfaces, 1))
for i in range(num_interfaces):
    rho_1, V_1 = properties[i]  # Upper layer (Layer i)
    rho_2, V_2 = properties[i + 1]  # Lower layer (Layer i+1)
    R = (rho_2 * V_2 - rho_1 * V_1) / (rho_2 * V_2 + rho_1 * V_1)
    reflection_coefficients[i] = R

# Create a 2D profile by repeating the reflection coefficients
rc_2d_profile = np.tile(reflection_coefficients, (1, num_samples))

# Generate a random frequency from uniform distribution
frequency = np.random.uniform(f_min, f_max)
print(f"Using random frequency: {frequency:.2f} Hz")

# Generate the Ricker wavelet
wavelet = ricker_wavelet(frequency, dt, t_max)

# Convolve the reflection coefficient profile with the Ricker wavelet
# seismic_trace = convolve(rc_2d_profile.flatten(), wavelet, mode='same')
seismic_trace = rc_2d_profile.flatten()

# Add Gaussian noise to simulate real-world data
noise_level = 0.1  # Standard deviation of the Gaussian noise
noise = np.random.normal(0, noise_level, seismic_trace.shape)
# seismic_trace_with_noise = (seismic_trace + noise)
seismic_trace_with_noise = seismic_trace

# Plotting the synthetic seismic trace
plt.figure(figsize=(10, 6))
plt.imshow(seismic_trace_with_noise.reshape(num_interfaces, num_samples), aspect='auto', cmap='gray', origin='lower')
plt.colorbar(label='Amplitude')
plt.title('Synthetic Seismic Section with Gaussian Noise')
plt.ylabel('Time (samples)')
plt.xlabel('Layer Interfaces')
plt.show()
