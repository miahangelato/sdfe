from django.urls import path
from .views import EventView

urlpatterns = [
    path('api/events/', EventView.as_view(), name='events'),  # List all or create a new event
    path('api/events/<int:id>/', EventView.as_view(), name='event-detail'),  # Retrieve, update, or delete an event by ID
]
