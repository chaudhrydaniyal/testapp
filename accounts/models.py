from django.db import models
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from datetime import date
from django.core.exceptions import ValidationError

# Create your models here.
class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)
    code = models.CharField(max_length=255, null=True, default=None)
    room_uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    online = models.BooleanField(default=False)
    last_seen = models.DateTimeField(null=True)
    num_of_docs = models.PositiveIntegerField(default=100,verbose_name='Maximum Number of Documents') #maximum num of docs
    num_of_sources = models.PositiveIntegerField(default=100,verbose_name='Maximum Number of sources') #maximum num of sources
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ("username", "first_name", "last_name")
    def __str__(self):
        return self.username