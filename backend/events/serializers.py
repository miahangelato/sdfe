from rest_framework import serializers
# from .models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Event

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['name', 'date', 'organizer', 'location', 'description']