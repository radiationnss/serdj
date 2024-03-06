import traceback
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponseServerError
from .predict import prediction
from .models import Predicted
from .serializers import PredictedSerializer
import soundfile as sf
import librosa
from .speechtotxt import silence_or_not, text_from_speech
from .sentiment import top_emotions




class AudioPredictionSentimentView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            audio_file = request.FILES.get('file')
            if not audio_file:
                return Response({"error": "No audio file provided"}, status=status.HTTP_400_BAD_REQUEST)

            temp_path = './media/temp_audio.wav'
            with open(temp_path, 'wb') as f:
                for chunk in audio_file.chunks():
                    f.write(chunk)

            converted_path = './media/temp_audio.wav'
            data, sr = librosa.load(temp_path)
            sf.write(converted_path, data, sr)

            if silence_or_not(converted_path):
                prediction_result = prediction(temp_path)
                txt = text_from_speech(temp_path)
                print(txt)
                sentiment = top_emotions(txt)
                sentiment_dict = dict(sentiment)
                user = request.user
                new_prediction = Predicted(user=user, predicted_value=prediction_result)
                new_prediction.save()
            else:
                prediction_result = "couldn't hear anything"
                txt = ""
                sentiment_dict = ""

            return Response(data={"prediction_result": prediction_result, "txt": txt, "sentiment": sentiment_dict}, status=status.HTTP_200_OK)

        except Exception as e:
            traceback.print_exc()  # This will print the full stack trace
            return HttpResponseServerError(content="Internal Server Error: " + str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class AudioPredictionView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            audio_file = request.FILES.get('file')
            if not audio_file:
                return Response({"error": "No audio file provided"}, status=status.HTTP_400_BAD_REQUEST)

            temp_path = './media/temp_audio.wav'
            with open(temp_path, 'wb') as f:
                for chunk in audio_file.chunks():
                    f.write(chunk)

            converted_path = './media/temp_audio.wav'
            data, sr = librosa.load(temp_path)
            sf.write(converted_path, data, sr)

            if silence_or_not(converted_path):
                prediction_result = prediction(temp_path)
                user = request.user
                new_prediction = Predicted(user=user, predicted_value=prediction_result)
                new_prediction.save()
            else:
                prediction_result = "couldn't hear anything"

            return Response(data=prediction_result, status=status.HTTP_200_OK)

        except Exception as e:
            traceback.print_exc()  # This will print the full stack trace
            return HttpResponseServerError(content="Internal Server Error: " + str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PredictionHistoryView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            # Get the prediction history for the authenticated user
            prediction_history = Predicted.objects.filter(user=request.user)

            # Serialize the prediction history
            serializer = PredictedSerializer(prediction_history, many=True)
            print(serializer)
            return Response(data=serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            print("Error:", str(e))
            return Response(data={"detail": "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)