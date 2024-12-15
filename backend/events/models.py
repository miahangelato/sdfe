from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Event(models.Model):
    name = models.CharField(max_length=255, verbose_name="Event Name")
    date = models.DateField(verbose_name="Event Date")
    organizer = models.ForeignKey(  # Use ForeignKey for a relation
        User, 
        on_delete=models.CASCADE,  # Delete events if the organizer is deleted
        verbose_name="Organizer",
        related_name="events"  # Optional: allows reverse query like user.events.all()
    )
    location = models.CharField(blank=True, max_length=255, null=True, verbose_name="Location")
    description = models.TextField(blank=True, null=True, verbose_name="Event Description")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-date']
        verbose_name = "Event"
        verbose_name_plural = "Events"
