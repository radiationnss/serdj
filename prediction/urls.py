# appname/urls.py
from django.urls import path
from .views import AudioPredictionView, PredictionHistoryView, AudioPredictionSentimentView

urlpatterns = [
    path('predict-emotion/', AudioPredictionView.as_view(), name='predict_emotion'),
    path('history/', PredictionHistoryView.as_view(), name='prediction_history'),
    path('prediction-emotion-sentiment/', AudioPredictionSentimentView.as_view(), name='prediction_history_sentiment'),
]
