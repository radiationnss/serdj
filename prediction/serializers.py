from rest_framework import serializers
from .models import Predicted

class PredictedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Predicted
        fields = ['user', 'predicted_value', 'predicted_txt', 'created_at']
        read_only_fields = ['user', 'created_at']