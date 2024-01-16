# admin.py

from django.contrib import admin
from .models import Predicted

@admin.register(Predicted)
class PredictedAdmin(admin.ModelAdmin):
    list_display = ('user', 'predicted_value', 'created_at')
    search_fields = ('user__email', 'predicted_value')  # Enable searching by user email and predicted value
    list_filter = ('created_at',)  # Enable filtering by creation date
