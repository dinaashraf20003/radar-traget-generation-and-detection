# Radar target generation and detection project for Udacity sensor fusion nano degree

![Project Layout](https://github.com/dinaashraf20003/radar-traget-generation-and-detection/assets/73821958/f491e861-c204-4ff6-975d-fbfbc79aaa1b)

# Steps
- Configure the FMCW waveform based on the system requirements.
- Define the range and velocity of target and simulate its displacement.
- For the same simulation loop process the transmit and receive signal to determine the beat signal
- Perform Range FFT on the received signal to determine the Range
- Towards the end, perform the CFAR processing on the output of 2nd FFT to display the target.

# Radar System Requirements
![Radar Specs](https://github.com/dinaashraf20003/radar-traget-generation-and-detection/assets/73821958/c281708e-2c60-4f10-bb85-0e190c972d1d)

# Project Output

![Figure_5](https://github.com/dinaashraf20003/radar-traget-generation-and-detection/assets/73821958/8b7bfe47-8d09-4c89-815d-e9c382308545)


![Figure_6](https://github.com/dinaashraf20003/radar-traget-generation-and-detection/assets/73821958/fb5c783c-ca54-4330-a1c6-c2c9b1142f0f)

# Scripts
## FFT
- Function: Fast Fourier Transform is used to convert the signal from time domain to frequency domain. Conversion to frequency domain is important to do the spectral analysis of the signal and determine the shifts in frequency due to range and doppler.
- Output:
 ![Figure_2](https://github.com/dinaashraf20003/radar-traget-generation-and-detection/assets/73821958/ac0f5a08-75b7-433d-8429-927d2c8698bd)

## 2D FFT
- Function: The output of the first FFT gives the beat frequency, amplitude, and phase for each target. This phase varies as we move from one chirp to another (one bin to another on each row) due to the target’s small displacements. Once the second FFT is implemented it determines the rate of change of phase, which is nothing but the doppler frequency shift.
- Output
  
## 1D CFAR



## radar-target-generation-and-detection
