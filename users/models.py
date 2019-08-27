from django.db import models
from django.contrib.auth.models import User
from blog.storage import OverwriteStorage
from django.dispatch import receiver
from django.db.models.signals import post_save

def user_avatar_path(instance, filename):
    return "user_{0}/avatar/{1}".format(instance.user.id, filename)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
    date_birth = models.DateField(blank=True)
    about = models.TextField(max_length=500, blank=True)
    avatar = models.ImageField(upload_to=user_avatar_path, storage=OverwriteStorage(), default='default/anonymous.png')  
    friends = models.ManyToManyField('Profile', blank=True)

    def __str__(self):
        return str(self.user.username)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.user_profile.save()