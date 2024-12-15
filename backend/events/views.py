from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Event
from .serializers import EventSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class EventView(APIView):
    def get(self, request, id=None):
        """
        Retrieve all events or a specific event by ID. Anyone (including Attendees) can view events.
        """
        if id:
            try:
                event = Event.objects.get(id=id)
                serializer = EventSerializer(event)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Event.DoesNotExist:
                return Response({"error": "Event not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            events = Event.objects.all()
            serializer = EventSerializer(events, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Create a new event. Only the user who is an organizer can create an event.
        """
        # Check if the user is an organizer
        if request.user.is_organizer != True:
            return Response({"error": "You are not authorized to create events"}, status=status.HTTP_403_FORBIDDEN)
        
        organizer_id = request.data.get('organizer')
        
        # Ensure the organizer is valid
        try:
            organizer = User.objects.get(id=organizer_id)
        except User.DoesNotExist:
            return Response({"error": "Organizer does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the current user is the organizer
        if request.user.id != organizer.id:
            return Response({"error": "You are not authorized to create this event"}, status=status.HTTP_403_FORBIDDEN)
        
        # Proceed to create the event
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id=None):
        """
        Update an existing event. Only the organizer can update the event.
        """
        # Check if the user is an organizer
        if request.user.is_organizer != True:
            return Response({"error": "You are not authorized to update"}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            event = Event.objects.get(id=id)
        except Event.DoesNotExist:
            return Response({"error": "Event not found"}, status=status.HTTP_404_NOT_FOUND)

        # Ensure that the user making the request is the organizer
        if request.user.id != event.organizer.id:
            return Response({"error": "You are not authorized to update this event"}, status=status.HTTP_403_FORBIDDEN)

        serializer = EventSerializer(event, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id=None):
        """
        Delete an event. Only the organizer can delete the event.
        """
        # Check if the user is an organizer
        if request.user.is_organizer != True:
            return Response({"error": "You are not authorized to delete events"}, status=status.HTTP_403_FORBIDDEN)
        
        if request.user.id != event.organizer.id:
            return Response({"error": "You are not authorized to delete this event"}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            event = Event.objects.get(id=id)
        except Event.DoesNotExist:
            return Response({"error": "Event not found"}, status=status.HTTP_404_NOT_FOUND)

        # Ensure that the user making the request is the organizer
        if request.user.id != event.organizer.id:
            return Response({"error": "You are not authorized to delete this event"}, status=status.HTTP_403_FORBIDDEN)

        event.delete()
        return Response({"message": "Event deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
