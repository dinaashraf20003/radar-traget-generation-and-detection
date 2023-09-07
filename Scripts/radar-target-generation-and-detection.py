import numpy as np
import matplotlib.pyplot as plt

# Radar Specifications
max_range = 200
range_resolution = 1
radar_max_velocity = 100
fc = 77e9

speed_of_light = 3e8

# User Defined Range and Velocity of target
init_pos = 100
init_v = 10

# FMCW Waveform Generation

#Calculate the Bandwidth (B), Chirp Time (Tchirp) and Slope (slope) of the FMCW
#chirp using the requirements above.

B = speed_of_light / (2 * range_resolution)
t_sweep = 5.5
t_chirp = t_sweep * 2 * (max_range / speed_of_light)
slope = B / t_chirp

Nd = 128    #no of doppler cells
Nr = 1024   #no of range cells

# Timestamp for running the displacement scenario for every sample on each chirp
t = np.linspace(0, Nd * t_chirp, Nr * Nd)  #total time for samples

#Creating the vectors for Tx, Rx and Mix based on the total samples input
Tx = np.zeros(len(t))
Rx = np.zeros(len(t))
Mix = np.zeros(len(t))

#Similar vectors for range_covered and time delay
r_t = np.zeros(len(t))
td = np.zeros(len(t))

#Signal generation and Moving Target simulation

for i in range (len(t)):
    #For each time stamp update the Range of the Target for constant velocity
    r_t[i] = init_pos + (init_v * t[i])
    td[i] = (2 * r_t[i]) / speed_of_light

    #For each time sample we need update the transmitted and received signal.
    Tx[i] = np.cos(2*np.pi*(fc*t[i]+((slope*t[i]**2)/2)))
    Rx[i] = np.cos(2*np.pi*(fc*(t[i]-td[i])+((slope*(t[i]-td[i])**2)/2)))
    Mix[i] = Tx[i] * Rx[i]

# Range measurement

#reshape the vector into Nr*Nd array
Mix = Mix.reshape((Nr, Nd))
#run the FFT on the beat signal along the range bins dimension (Nr)
sig_fft = np.fft.fft(Mix,Nr,axis=0)
sig_fft = sig_fft / np.max(sig_fft) #normalize
#Take the absolute value of FFT output
sig_fft = np.abs(sig_fft)

#Output of FFT is double sided signal, but we are interested in only one side of the spectrum.
#Hence we throw out half of the samples
sig_fft = sig_fft[:Nr//2-1]

# RANGE DOPPLER RESPONSE
Mix = Mix.reshape((Nr, Nd))
sig_fft2 = np.fft.fft2(Mix, s=(Nr, Nd))
sig_fft2 = sig_fft2[:Nr//2, :Nd]
sig_fft2 = np.fft.fftshift(sig_fft2)
RDM = np.abs(sig_fft2)
RDM = 10 * np.log10(RDM)
doppler_axis = np.linspace(-100, 100, Nd)
range_axis = np.linspace(-200, 200, Nr//2) * (Nr//2 / 400)

# Plot Range Doppler Response
fig = plt.figure()
ax = fig.add_subplot(projection='3d')
doppler_axis, range_axis = np.meshgrid(doppler_axis, range_axis)
ax.plot_surface(doppler_axis, range_axis, RDM, cmap='viridis')
ax.set_title('Amplitude and Range From FFT2')
ax.set_xlabel('Speed')
ax.set_ylabel('Range')
ax.set_zlabel('Amplitude')
plt.show()

# CFAR implementation
T_r = 10 #Training cells
T_d = 8  #training band
G_r = 4  # Gaurd cells
G_d = 4  #gyard band
offset = 1.15

RDM = RDM / np.max(RDM) #Range doppler map

for i in range(T_r + G_r + 1, (Nr//2) - (T_r + G_r)):
    for j in range(T_d + G_d + 1, Nd - (T_d + G_d)):
        noise_level = 0
        
        for k in range(i - (T_r + G_r), i + (T_r + G_r) + 1):
            for l in range(j - (T_d + G_d), j + (T_d + G_d) + 1):
                if abs(i - k) > G_r or abs(j - l) > G_d:
                    noise_level += 10 ** (0.1 * RDM[k, l])
        
        threshold = 10 * np.log10(noise_level / (2 * (T_d + G_d + 1) * 2 * (T_r + G_r + 1) - (G_r * G_d) - 1))
        threshold += offset
        
        cell_under_test = RDM[i, j]

        if cell_under_test < threshold:
            RDM[i, j] = 0
        else:
            RDM[i, j] = 1

RDM[(RDM != 0) & (RDM != 1)] = 0

# Display CFAR output
fig = plt.figure()
ax = fig.add_subplot(projection='3d')
ax.plot_surface(doppler_axis, range_axis, RDM, cmap='viridis')
plt.colorbar(ax.plot_surface(doppler_axis, range_axis, RDM, cmap='viridis'), ax=ax)
ax.set_title('CA-CFAR Filtered RDM Surface Plot')
ax.set_xlabel('Speed')
ax.set_ylabel('Range')
ax.set_zlabel('Normalized Amplitude')
plt.show()

