from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Event
from .serializers import EventSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class EventView(APIView):
    """
    Handles all CRUD operations for Events:
    - GET /api/events: List all events
    - POST /api/events: Create a new event
    - PUT /api/events/{id}/update: Update an event by ID
    - DELETE /api/events/{id}/delete: Delete an event by ID
    """

    def get(self, request, id=None):
        """
        Retrieve all events or a specific event by ID.
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
        Create a new event.
        """
        # Ensure the organizer is valid before saving
        organizer_id = request.data.get('organizer')
        try:
            organizer = User.objects.get(id=organizer_id)
        except User.DoesNotExist:
            return Response({"error": "Organizer does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Proceed to create the event
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id=None):
        """
        Update an existing event by ID.
        """
        try:
            event = Event.objects.get(id=id)
        except Event.DoesNotExist:
            return Response({"error": "Event not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = EventSerializer(event, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id=None):
        """
        Delete an event by ID.
        """
        try:
            event = Event.objects.get(id=id)
        except Event.DoesNotExist:
            return Response({"error": "Event not found"}, status=status.HTTP_404_NOT_FOUND)

        event.delete()
        return Response({"message": "Event deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
