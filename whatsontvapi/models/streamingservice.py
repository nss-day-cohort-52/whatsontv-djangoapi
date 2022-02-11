from django.db import models

class StreamingService(models.Model):
    name = models.CharField(max_length=55)
    