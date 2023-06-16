# Audio Denoising
# Author: Long Nguyen-Vu & ChatGPT, code adapted from https://github.com/AP-Atul/Audio-Denoising/tree/master
# Date: 2023-06-15

import pywt
import librosa
from tqdm import tqdm
import soundfile as sf
import numpy as np


def mad(arr):
    """ Median Absolute Deviation: a "Robust" version of standard deviation.
        Indices variability of the sample.
        https://en.wikipedia.org/wiki/Median_absolute_deviation
    """
    arr = np.ma.array(arr).compressed()
    med = np.median(arr)
    return np.median(np.abs(arr - med))


class DeNoise:
    """
    process the input signal to remove noise
    inputSignal: np.ndarray
    outputSignal: np.ndarray
    sample_rate: 16000
    """
    def __init__(self, inputSignal):
        self.inputSignal = inputSignal
        self.outputSignal = None

  
    def process(self, sr=16000) -> np.ndarray:
        inputSignal = self.inputSignal
        rate = sr
        duration = librosa.get_duration(y=inputSignal, sr=sr)
        output_signal = []

        block_size = int(rate * duration * 0.10)  # Block size as 10% of the duration

        for block_start in tqdm(range(0, len(inputSignal), block_size)):
            block_end = block_start + block_size
            block = inputSignal[block_start:block_end]

            coefficients = pywt.wavedec(block, 'db4', mode='per', level=2)

            # Getting variance of the input signal
            sigma = mad(coefficients[-1])

            # VISU Shrink thresholding by applying the universal threshold proposed by Donoho and Johnstone
            thresh = sigma * np.sqrt(2 * np.log(len(block)))

            # Thresholding using the noise threshold generated
            coefficients[1:] = (pywt.threshold(i, value=thresh, mode='soft') for i in coefficients[1:])

            # Getting the clean signal as in the original form
            clean = pywt.waverec(coefficients, 'db4', mode='per')
            output_signal.extend(clean)

        return np.array(output_signal)
    
"""
# Test
# TODO soundfile.py", line 1021, in write assert written == len(data) AssertionError
# but we can still get the output file. 

# np.seterr(divide='ignore', invalid='ignore')

def read_audio_file(file_path):
    audio_data, _ = sf.read(file_path)
    return audio_data

def save_audio_file(signal, file_path, sample_rate=16000):
    sf.write(file_path, signal, sample_rate)

file_path = './vinyl.wav'
inputSignal = read_audio_file(file_path)
print(len(inputSignal))
deNoiser = DeNoise(inputSignal)
outputSignal = deNoiser.process()
print(len(outputSignal))

save_audio_file(outputSignal, file_path='./test.test/vinyl_denoised.flac')
"""
