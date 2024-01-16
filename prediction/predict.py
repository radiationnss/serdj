import numpy as np
from tensorflow.keras.models import Sequential, model_from_json
import pickle
import librosa

json_file_path = './prediction/modelharu/CNN_model.json'
weights_file_path = "./prediction/modelharu/best_model1_weights.h5"
scaler2_file_path = "./prediction/modelharu/scaler2.pickle"
encoder2_file_path = "./prediction/modelharu/encoder2.pickle"

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

def zcr(data,frame_length,hop_length):
    zcr=librosa.feature.zero_crossing_rate(data,frame_length=frame_length,hop_length=hop_length)
    return np.squeeze(zcr)

def rmse(data, frame_length=2048, hop_length=512):
    # Compute the spectrogram
    spec = np.abs(librosa.stft(data, n_fft=frame_length, hop_length=hop_length))

    # Calculate RMS from the spectrogram
    rmse = librosa.feature.rms(S=spec, frame_length=frame_length, hop_length=hop_length)

    return np.squeeze(rmse)

def mfcc(data, sr, frame_length=2048, hop_length=512, flatten: bool = True):
    # Compute the spectrogram
    spec = np.abs(librosa.stft(data, n_fft=frame_length, hop_length=hop_length))

    # Calculate MFCCs from the spectrogram
    mfcc = librosa.feature.mfcc(S=librosa.power_to_db(spec), sr=sr)

    return np.squeeze(mfcc.T) if not flatten else np.ravel(mfcc.T)

def extract_features(data,sr=22050,frame_length=2048,hop_length=512):
    result=np.array([])
    
    result=np.hstack((result,
                      zcr(data,frame_length,hop_length),
                      rmse(data,frame_length,hop_length),
                      mfcc(data,sr,frame_length,hop_length)
                     ))
    return result

def get_predict_feat(path):
    d, s_rate= librosa.load(path, duration=2.5, offset=0.6)
    res=extract_features(d)
    result=np.array(res)
    result=np.reshape(result,newshape=(1,2376))
    i_result = scaler2.transform(result)
    final_result=np.expand_dims(i_result, axis=2)
    
    return final_result


emotions1={1:'Neutral', 2:'Calm', 3:'Happy', 4:'Sad', 5:'Angry', 6:'Fear', 7:'Disgust',8:'Surprise'}
def prediction(path1):
    res=get_predict_feat(path1)
    predictions=loaded_model.predict(res)
    y_pred = encoder2.inverse_transform(predictions)
    print(y_pred[0][0])
    return(y_pred[0][0])