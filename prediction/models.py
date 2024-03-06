from django.db import models
from users.models import UserAccount

class Predicted(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    predicted_value = models.CharField(max_length=255)  # Adjust the max_length as needed
    predicted_txt = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.predicted_value} - {self.created_at}"
