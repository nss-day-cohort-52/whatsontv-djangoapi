from django.db import models

class Actor(models.Model):
    name = models.CharField(max_length=55)
    