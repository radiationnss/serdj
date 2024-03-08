import numpy as np
from tensorflow.keras.models import Sequential, model_from_json
import pickle
import scipy.signal
from scipy.io import wavfile
from scipy.fftpack import dct
import os
from pydub import AudioSegment


json_file_path = './prediction/modelharuO/CNN_model.json'
weights_file_path = "./prediction/modelharuO/best_model1_weights.h5"
scaler2_file_path = "./prediction/modelharuO/scaler2.pickle"
encoder2_file_path = "./prediction/modelharuO/encoder2.pickle"

try:
    # Load the JSON file
    json_file = open(json_file_path, 'r')
    loaded_model_json = json_file.read()
    json_file.close()

    # Load the model architecture from JSON
    loaded_model = model_from_json(loaded_model_json)

    # Load the weights into the model
    loaded_model.load_weights(weights_file_path)

    print("Models loaded successfully.")

except Exception as e:
    print("Error loading models:", str(e))


try:
    with open(scaler2_file_path, 'rb') as f:
        scaler2 = pickle.load(f)

    with open(encoder2_file_path, 'rb') as f:
        encoder2 = pickle.load(f)

    print("pickle loaded")

except Exception as e:
    print("Error loading pickel:", str(e))

def preemphasis(signal, coefficient=0.97):
    return np.append(signal[0], signal[1:] - coefficient * signal[:-1])

def compute_mfccs(signal, sample_rate, n_mfcc=40, n_fft=1200, hop_length=512):
    # Apply pre-emphasis
    signal = preemphasis(signal)

    # Compute the spectrogram
    _, _, Sxx = scipy.signal.spectrogram(signal, fs=sample_rate, nperseg=n_fft, noverlap=hop_length)

    # Apply the Mel filter bank
    mel_filterbank = mel_filter_bank(sample_rate, n_fft, n_mels=n_mfcc)
    mel_S = np.dot(mel_filterbank, Sxx)

    # Log compression
    log_mel_S = np.log(mel_S + 1e-9)

    # Compute DCT
    mfcc = dct(log_mel_S, type=2, axis=0, norm='ortho')[:n_mfcc]

    return mfcc

def mel_filter_bank(sr, n_fft, n_mels=128):
    mel_min = 0.0
    mel_max = mel(sr / 2)
    mel_points = np.linspace(mel_min, mel_max, n_mels + 2)
    hz_points = mel_to_hz(mel_points)
    bin_points = np.floor((n_fft + 1) * hz_points / sr).astype(int)
    filter_bank = np.zeros((n_mels, n_fft // 2 + 1))

    for i in range(1, n_mels + 1):
        filter_bank[i - 1, bin_points[i - 1]:bin_points[i + 1]] = (
            np.arange(bin_points[i - 1], bin_points[i + 1]) - bin_points[i - 1]
        ) / (bin_points[i + 1] - bin_points[i - 1])

    filter_bank /= np.sum(filter_bank, axis=1)[:, np.newaxis]

    return filter_bank

def mel(sr):
    return 2595 * np.log10(1 + sr / 700)

def mel_to_hz(mel):
    return 700 * (10 ** (mel / 2595) - 1)

def convert_aiff_to_wav(input_file, output_file):
    sound = AudioSegment.from_file(input_file, format="aiff")
    sound.export(output_file, format="wav")

def load_data(filename):
    _, file_extension = os.path.splitext(filename)
    if file_extension.lower() == '.wav':
        sample_rate, data = wavfile.read(filename)
        # Convert audio data to floating-point format
        data = data.astype(np.float32)
    else:
        # If not WAV, convert to WAV
        converted_filename = 'converted.wav'
        convert_aiff_to_wav(filename, converted_filename)
        sample_rate, data = wavfile.read(converted_filename)
        os.remove(converted_filename)

    return sample_rate, data

def extract_mfcc1(data, sample_rate, duration=3, offset=0.5):
    # Normalize the audio signal
    signal = data.astype(np.float32) / np.max(np.abs(data))

    # Select the desired portion of the audio based on duration and offset
    start_sample = int(offset * sample_rate)
    end_sample = start_sample + int(duration * sample_rate)
    signal = signal[start_sample:end_sample]

    # Compute MFCCs
    mfcc = compute_mfccs(signal, sample_rate)

    return np.mean(mfcc.T, axis=0)

def get_predict_feat(path):
    s_rate, d= load_data(path)
    res=extract_mfcc1(d, s_rate)
    result=np.array(res)
    result=np.reshape(result,newshape=(1,40))
    i_result = scaler2.transform(result)
    final_result=np.expand_dims(i_result, axis=2)
    
    return final_result

emotions1={1:'Neutral', 2:'Sad', 3:'Happy', 4:'Angry'}
def prediction(path1):
    res=get_predict_feat(path1)
    predictions=loaded_model.predict(res)
    y_pred = encoder2.inverse_transform(predictions)
    print(y_pred[0][0])
    return(y_pred[0][0])