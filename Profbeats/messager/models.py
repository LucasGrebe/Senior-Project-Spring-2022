from django.db import models

# Create your models here.

class Message(models.Model):
    sender = models.CharField(max_length=20)
    subject = models.CharField(max_length=50, blank=True, default='')
    recipient = models.CharField(max_length=20)
    text = models.TextField(max_length=1000)
    track_id = models.CharField(max_length=22, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)