from django.db import models

class TVShow(models.Model):
    name = models.CharField(max_length=55)
    num_of_seasons = models.IntegerField()
    streaming_service = models.ForeignKey("StreamingService", on_delete=models.CASCADE)
    #This many to many field does a LOT for us. 
    actors = models.ManyToManyField("Actor", through="TVActor")
    