import numpy as np
import librosa

def signaltonoise(a, axis=0, ddof=0):
    """
    The signal-to-noise ratio of the input data.

    Returns the signal-to-noise ratio of `a`, here defined as the mean
    divided by the standard deviation.

    Parameters
    ----------
    a : array_like
        An array_like object containing the sample data.
    axis : int or None, optional
        If axis is equal to None, the array is first ravel'd. If axis is an
        integer, this is the axis over which to operate. Default is 0.
    ddof : int, optional
        Degrees of freedom correction for standard deviation. Default is 0.

    Returns
    -------
    s2n : ndarray
        The mean to standard deviation ratio(s) along `axis`, or 0 where the
        standard deviation is 0.

    """
    a = np.asanyarray(a)
    m = np.mean(a, axis=axis)
    sd = np.std(a, axis=axis, ddof=ddof)
    return np.where(sd == 0, 0, m / sd)


# Load the audio file
audio_file = "../samples/DF_E_2000492.flac"
audio, sr = librosa.load(audio_file, sr=None)

# Calculate the signal-to-noise ratio (SNR)
snr = signaltonoise(audio)

# Print the SNR value
print("Signal-to-Noise Ratio (SNR):", snr)
