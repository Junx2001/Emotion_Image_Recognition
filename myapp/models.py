from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads/')
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    emotion = models.CharField(max_length=100,null=True)
    uploaded_time = models.DateTimeField(auto_now_add=True)

    