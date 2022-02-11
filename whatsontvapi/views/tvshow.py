from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from whatsontvapi.models import TVShow, StreamingService

class TVShowView(ViewSet):
    #Getting ONE TV Show
    def retrieve(self, request, pk): 
        # The ORM is digging into the database and finding the row whose PK matches the one sent in the URL.
        # Because the database tables were created by migrating the models, we can use the ORM on the TVShow model to access the database.
        # After line 13 runs, the tv show is a Python object (AKA an instance of the model class)
        tvshow = TVShow.objects.get(pk=pk)
        # Client side doesn't speak Python!
        # We take that Python object and turn it into JSON with the serializer
        serializer = TVShowSerializer(tvshow)
        # Gotta send the JSON back in the response to whoever requested it!
        return Response(serializer.data)
    
    #Getting ALL tv shows
    def list(self, request):
        # The ORM goes and gets ALL the rows in the database table created by the TVShow model.
        tvshows = TVShow.objects.all()
        #The Python objects are passed into the serializer to turn them all into JSON 
        #Gotta tell it there's more than one object to serialize! Hence the many=true
        serializer = TVShowSerializer(tvshows, many=True)
        return Response(serializer.data)
        
    def create(self, request):
        #Need to make sure the streaming service foreign key represents a real row in the database
        #So we use the ORM to go check that and give us the whole object
        streaming_service = StreamingService.objects.get(pk=request.data["streaming_service"])
        #We then use the create method to assemble a Python object that will then be sent to the database
        tvshow = TVShow.objects.create(
            name=request.data["name"],
            num_of_seasons=request.data["num_of_seasons"],
            streaming_service=streaming_service
        )
        #The set method will take care of the entries to the TVActor join table, since we put the many-to-many attribute on the TVShow model.
        tvshow.actors.set(request.data["actors"])
        #Still got to serialize, so we can send JSON back to the client!
        serializer = TVShowSerializer(tvshow)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk):
        #See lines 30 and 31
        streaming_service = StreamingService.objects.get(pk=request.data["streaming_service"])
        #Now we need to go get the tv show we're editing from the database
        #Notice it's the same way we do it in the retrieve?
        tvshow = TVShow.objects.get(pk=pk)
        
        #Even if we don't edit theses fields, we need to match up the values to the keys
        #This is because we're still receiving a full object from the client, and the method needs to know what to do with everything
        tvshow.name = request.data["name"]
        tvshow.num_of_seasons = request.data["num_of_seasons"]
        tvshow.streaming_service = streaming_service
        #Same as line 39! The "set" method does a LOT for us, because it knows to adjust the TVActors join table based on what was sent back in the updated array on the object!
        tvshow.actors.set(request.data["actors"])
        #Not serializing because we don't need to send it back. 
        tvshow.save()
        
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk): 
        #Pretty simple. Same as retrieve, so we know which one we're deleting!
        #Imagine how disastrous it'd be if we did "all" instead of "get" and had 100s of tv shows in our database!
        tvshow = TVShow.objects.get(pk=pk)
        tvshow.delete()
        
        return Response(None, status=status.HTTP_204_NO_CONTENT)
        
        
#Turns the Python objects into JSON!
class TVShowSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = TVShow
        #Shorthand if you don't need to specify which fields you need
        fields = '__all__'
        #Equivalent to "expand" when we were using JSON server
        depth = 1