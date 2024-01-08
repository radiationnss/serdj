from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import SuspiciousOperation
from django.http import HttpResponseServerError
from .predict import prediction

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

            return Response(data=prediction_result, status=status.HTTP_200_OK)

        except SuspiciousOperation as e:
            # This exception is raised for certain suspicious operations
            return HttpResponseServerError(content=str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as e:
            # Log the error for debugging purposes
            print("Error:", str(e))
            return HttpResponseServerError(content="Internal Server Error", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
