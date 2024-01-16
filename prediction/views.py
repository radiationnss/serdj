from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import SuspiciousOperation
from django.http import HttpResponseServerError
from .predict import prediction
from .models import Predicted
from .serializers import PredictedSerializer


class AudioPredictionView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            # Assuming the file is sent as part of the POST request
            audio_file = request.FILES['file']  # Change 'file' to the name you are using in the FormData

            # Save the uploaded file to a temporary location
            temp_path = './media/temp_audio.wav'  # Change the path to your desired location
            with open(temp_path, 'wb') as f:
                for chunk in audio_file.chunks():
                    f.write(chunk)
            # Get prediction
            prediction_result = prediction(temp_path)

            user = request.user  # Assuming the user is authenticated
            new_prediction = Predicted(user=user, predicted_value=prediction_result)
            new_prediction.save()

            # Serialize the new prediction to include in the response
            serializer = PredictedSerializer(new_prediction)
            print(serializer)

            return Response(data=prediction_result, status=status.HTTP_200_OK)

        except SuspiciousOperation as e:
            # This exception is raised for certain suspicious operations
            return HttpResponseServerError(content=str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as e:
            # Log the error for debugging purposes
            print("Error:", str(e))
            return HttpResponseServerError(content="Internal Server Error", status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PredictionHistoryView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            # Get the prediction history for the authenticated user
            prediction_history = Predicted.objects.filter(user=request.user)
            
            # Serialize the prediction history
            serializer = PredictedSerializer(prediction_history, many=True)
            
            return Response(data=serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            # Log the error for debugging purposes
            print("Error:", str(e))
            return Response(data={"detail": "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
