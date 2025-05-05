from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class CustomUser(AbstractUser):
    address = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return self.username
    

class Room(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    room_id = models.CharField(max_length=100, unique=True)
    host = models.CharField(max_length=100)
    guest_count = models.IntegerField(default=0)
    max_guests = models.IntegerField(default=4)
    created_at = models.DateTimeField(auto_now_add=True)