# SIGNAL TO NOISE RATIO (SNR) CALCULATION
# We re-implemeted the SNR calculation so that it takes into account the noisy signal
# and presumably the denoised signal, bandpassed signal and adversarial signal.
# Reference: https://github.com/hrtlacek/SNR/blob/main/SNR.ipynb


import numpy as np
import librosa


def read_signal(inputSignal):
    y, _ = librosa.load(inputSignal, sr=None)
    return y


def signalPower(x):
    return np.average(x**2)


def SNR(signal, noise):
    powS = signalPower(signal)
    powN = signalPower(noise)
    # return 10 * np.log10((powS - powN) / powN)
    return 10 * np.log10(powS / powN)


def SNRsystem(inputSig, dnSig, bpSig, advSig):
    
    minLen = min(len(inputSig), len(dnSig), len(bpSig), len(advSig))
  
    noiseDN = inputSig[:minLen] - dnSig[:minLen]
    noiseBP = inputSig[:minLen] - bpSig[:minLen]
    noiseADV = inputSig[:minLen] - advSig[:minLen]

    powI = signalPower(inputSig)
    powD = signalPower(dnSig)
    powB = signalPower(bpSig)
    powerA = signalPower(advSig)
    
    powN1 = signalPower(noiseDN)
    powN2 = signalPower(noiseBP)
    powN3 = signalPower(noiseADV)
    
    print("Power of Input Signal -- powI: ", powI)
    print("Power of Denoised Signal -- powD: ", powD)
    print("Power of Bandpassed Signal -- powB: ", powB)
    print("Power of Adversarial Signal -- powA: ", powerA)
    print(f"Power of NoiseDN = {powN1}, NoiseBP = {powN2}, NoiseADV = {powN3}")

    # return 10 * np.log10((powS - powN) / powN)
    return SNR(dnSig, noiseDN), SNR(bpSig, noiseBP), SNR(advSig, noiseADV)

def scipy_snr(a, axis=0, ddof=0):git
    # The scipy_snr function remains unchanged
    a = np.asanyarray(a)
    m = np.mean(a, axis=axis)
    sd = np.std(a, axis=axis, ddof=ddof)
    return np.where(sd == 0, 0, m / sd)




in_sig = "./samples/LA_E_1239941_original.flac"
out_sig = "./samples/LA_E_1239941_denoised.flac"
bp_sig = "./samples/LA_E_1239941_bandpassed.flac"
adv_sig = "./samples/LA_E_1239941_adv.wav"

y_in = read_signal(in_sig)
y_out = read_signal(out_sig)
y_bp = read_signal(bp_sig)
y_adv = read_signal(adv_sig)
min_len = min(len(y_in), len(y_out))

print("SNR systems: ", SNRsystem(y_in[:min_len], y_out[:min_len], y_bp, y_adv))


# import os

# adv_dir = "./samples/adv"  # Path to the 'adv' directory

# # Get a list of all files in the 'adv' directory
# adv_files = os.listdir(adv_dir)

# # Loop through each file in the 'adv' directory
# for adv_file in adv_files:
#     if adv_file.endswith(".wav"):
#         # If the file is in 'adv' directory and has ".wav" extension
#         # Remove the "_adv.wav" suffix to get the corresponding file names in other directories
#         file_name = adv_file[:-8]  # Assuming "_adv.wav" suffix is always 8 characters long

#         # Form the file paths for other directories
#         original_file = os.path.join("./samples/original", file_name + ".flac")
#         denoised_file = os.path.join("./samples/denoised", file_name + ".flac")
#         bandpassed_file = os.path.join("./samples/bandpassed", file_name + ".flac")
#         adv_file = os.path.join(adv_dir, adv_file)

#         # Read the signals from the files
#         y_in = read_signal(original_file)
#         y_out = read_signal(denoised_file)
#         y_bp = read_signal(bandpassed_file)
#         y_adv = read_signal(adv_file)

#         min_len = min(len(y_in), len(y_out), len(y_bp), len(y_adv))

#         # Perform the calculations and print the results
#         snr_denoised, snr_bandpassed, snr_adv = SNRsystem(y_in[:min_len], y_out[:min_len], y_bp[:min_len], y_adv[:min_len])

#         print(f"SNR for {adv_file}: Denoised: {snr_denoised}, Bandpassed: {snr_bandpassed}, Adversarial: {snr_adv}")
