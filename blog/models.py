from django.db import models
from django.contrib.auth.models import User
from picturas import settings
from django.utils import timezone

def user_directory_path(instance, filename):
    return "user_{0}/posts/{1}".format(instance.author.id, filename)

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(max_length=500, blank=True)
    image = models.ImageField(upload_to=user_directory_path)
    likes = models.ManyToManyField(User, related_name='users_likes', blank=True)
    date_pub = models.DateTimeField(default=timezone.now)
    date_edit = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return "author {0} date {1} likes {2}".format(self.author.username, self.date_pub, self.get_likes)
    
    @property
    def get_likes(self):
        return self.likes.count()

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=700, blank=False)
    in_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    date_publish = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "{0} : {1}".format(self.author, self.text)