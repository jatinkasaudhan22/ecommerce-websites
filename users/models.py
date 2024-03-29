from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contact = models.CharField(max_length=14)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    profile_pic = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Meta:
    db_table = 'profile'


# def __str__(self):
#     return self.user.username