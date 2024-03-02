from django.db import models
from django.contrib.auth.models import User

#Used the Django built-in User Model for user account creation.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    facebook = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.user.username
