from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=150)
    signup_confirmation = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

class Saved_Articles(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    source = models.CharField(max_length=5000, blank=True)
    author = models.CharField(max_length=5000, blank=True)
    title = models.CharField(max_length=5000, blank=True)
    description = models.CharField(max_length=5000, blank=True)
    url = models.CharField(max_length=5000, blank=True)
    image = models.CharField(max_length=5000, blank=True)
    published = models.CharField(max_length=5000, blank=True)
    content = models.CharField(max_length=5000, blank=True)
    totalResults = models.CharField(max_length=5000, blank=True)
    preference = models.CharField(max_length=5000,blank=True)

    def __str__(self):
        return (self.user.username + "'s Articles")

@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        Saved_Articles.objects.create(user=instance)
    instance.profile.save()

class News(models.Model):
    source = models.CharField(max_length=120)
    title = models.CharField(max_length=120)
    author = models.CharField(max_length=120)
    publish_date = models.DateTimeField()

    def __str__(self):
        return self.title
