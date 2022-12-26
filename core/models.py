from uuid import uuid4

from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    REQUIRED_FIELDS = []


class Member(models.Model):
    # Link to the Django User Model
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    id = models.UUIDField(primary_key=True, default=uuid4)  # Creating a custom GUID (32char)

    contacts = models.TextField(null=True, blank=True)

    # => created_events field from Event model

    # => invited_events field from EventParticipant model

    @property
    def get_id(self):
        return self.id




class Event(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)  # Creating a custom GUID (32char)

    creator = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        related_name='created_events'
    )

    title = models.TextField()

    start_date = models.TextField()
    end_date = models.TextField(null=True, blank=True)

    description = models.TextField(null=True, blank=True)

    location = models.TextField(null=True, blank=True)

    # => participants field from EventParticipant model
    @property
    def get_id(self):
        return self.id


class EventParticipant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)  # Creating a custom GUID (32char)

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='participants')

    invited_member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='invited_events')

    acceptedStatus = models.BooleanField(default=False)

    class Meta:
        # Unique constraint : Only one invited_member - event pair allowed
        unique_together = [['event', 'invited_member']]

    @property
    def get_event_id(self):
        return self.event.id

