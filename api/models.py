from django.db import models

# Create your models here.
    # accounts/models.py


from django.db import models
from django.utils import timezone
from django.db import models
import uuid
# Create your models here.
class Request_approve(models.Model):
    uuid_id = models.UUIDField(default=uuid.uuid4)
    emal = models.CharField(max_length=100)
    transaction_id = models.CharField(max_length=100)
    image=models.ImageField(upload_to='images/')
    text = models.TextField()
    is_approved = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.emal
    
    


class User_Table(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    refresh_token = models.CharField(max_length=256, blank=True, null=True)
    token = models.CharField(max_length=256, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    date_joined = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []



    def __str__(self):
        return self.email