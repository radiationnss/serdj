# appname/urls.py
from django.urls import path
from .views import AudioPredictionView, PredictionHistoryView, AudioPredictionSentimentView, delete_user_predictions

urlpatterns = [
    path('predict-emotion/', AudioPredictionView.as_view(), name='predict_emotion'),
    path('history/', PredictionHistoryView.as_view(), name='prediction_history'),
    path('prediction-emotion-sentiment/', AudioPredictionSentimentView.as_view(), name='prediction_history_sentiment'),
    path('delete-predictions/', delete_user_predictions, name='delete_user_predictions'),

]
