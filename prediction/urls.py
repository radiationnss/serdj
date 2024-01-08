# appname/urls.py
from django.urls import path
from .views import AudioPredictionView

urlpatterns = [
    path('predict-emotion/', AudioPredictionView.as_view(), name='predict_emotion'),
]
