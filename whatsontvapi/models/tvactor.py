from django.db import models

#We wouldn't make a viewset for this one, because it's all taken care of by the "set" method we use inside our TVShow view's methods! 
class TVActor(models.Model):
    tvshow = models.ForeignKey("TVShow", on_delete=models.CASCADE)
    actor = models.ForeignKey("Actor", on_delete=models.CASCADE)

    