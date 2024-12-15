from django.urls import path
from .views import EventView

urlpatterns = [
    path('list/', EventView.as_view(), name='events'),  # List all or create a new event
    path('<int:id>', EventView.as_view(), name='event-detail'),  # Retrieve, update, or delete an event by ID
]
