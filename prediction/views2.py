from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import SuspiciousOperation
from django.http import HttpResponseServerError
import numpy as np
from tensorflow.keras.models import model_from_json
import pickle
import librosa

emotions1 = {1: 'Neutral', 2: 'Calm', 3: 'Happy', 4: 'Sad', 5: 'Angry', 6: 'Fear', 7: 'Disgust', 8: 'Surprise'}

json_file_path = './prediction/modelharu/CNN_model.json'
weights_file_path = "./prediction/modelharu/best_model1_weights.h5"
scaler2_file_path = "./prediction/modelharu/scaler2.pickle"
encoder2_file_path = "./prediction/modelharu/encoder2.pickle"

# Load the model and other necessary files when the module is imported
with open(json_file_path, 'r') as json_file:
    loaded_model_json = json_file.read()

loaded_model = model_from_json(loaded_model_json)
loaded_model.load_weights(weights_file_path)

with open(scaler2_file_path, 'rb') as scaler_file:
    scaler2 = pickle.load(scaler_file)

with open(encoder2_file_path, 'rb') as encoder_file:
    encoder2 = pickle.load(encoder_file)

class AudioPredictionView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            # Assuming the file is sent as part of the POST request
            audio_file = request.FILES['file']  # Change 'file' to the name you are using in the FormData

            # Save the uploaded file to a temporary location
            temp_path = './media/temp_audio.wav'  # Change the path to your desired location
            # with open(temp_path, 'wb') as f:
            #     for chunk in audio_file.chunks():
            #         f.write(chunk)

            # Get prediction
            prediction_result = self.predict_emotion(temp_path)

            return Response(content=prediction_result, status=status.HTTP_200_OK)

        except SuspiciousOperation as e:
            # This exception is raised for certain suspicious operations
            return HttpResponseServerError(content=str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as e:
            # Log the error for debugging purposes
            print("Error:", str(e))
            return HttpResponseServerError(content="Internal Server Error", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def predict_emotion(self, path):
        res = self.get_predict_feat(path)
        predictions = loaded_model.predict(res)
        y_pred = encoder2.inverse_transform(predictions)
        return emotions1[y_pred[0][0]]

    def get_predict_feat(self, path):
        d, s_rate = librosa.load(path, duration=2.5, offset=0.6)
        res = self.extract_features(d)
        result = np.array(res)

        print("Shapes before reshape:", result.shape)

        # Assuming the number of features expected by the model is 2376
        result = np.reshape(result, newshape=(1, 2376))

        print("Shapes after reshape:", result.shape)

        i_result = scaler2.transform(result)
        final_result = np.expand_dims(i_result, axis=2)

        print("Shapes after transform:", final_result.shape)

        return final_result


    def extract_features(self, data, sr=22050, frame_length=2048, hop_length=512):
        result=np.array([])
    
        result=np.hstack((result,
                        self.zcr(data,frame_length,hop_length),
                        self.rmse(data,frame_length,hop_length),
                        self.mfcc(data,sr,frame_length,hop_length)
                        ))
        return result


    def zcr(self, data, frame_length, hop_length):
        zcr = librosa.feature.zero_crossing_rate(data, frame_length=frame_length, hop_length=hop_length)
        return np.squeeze(zcr)

    def rmse(self, data, frame_length=2048, hop_length=512):
        spec = np.abs(librosa.stft(data, n_fft=frame_length, hop_length=hop_length))
        
        rmse = librosa.feature.rms(S=spec, frame_length=frame_length, hop_length=hop_length)
        return rmse

    def mfcc(self, data, sr, frame_length=2048, hop_length=512, flatten: bool = True):
        spec = np.abs(librosa.stft(data, n_fft=frame_length, hop_length=hop_length))
        mfcc = librosa.feature.mfcc(S=librosa.power_to_db(spec), sr=sr)
        return np.squeeze(mfcc.T) if not flatten else np.ravel(mfcc.T)
