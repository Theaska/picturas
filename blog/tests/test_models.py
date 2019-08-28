from django.test import TestCase, override_settings
from blog.models import *
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
import os 
import codecs
import tempfile 

class TestProfileModel(TestCase):

    def test_create_profile_without_avatar(self):
        user = User.objects.create_user(username='user', password='122334')
        self.assertEqual(user.user_profile.avatar, 'default/anonymous.png')
    

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_create_profile_with_avatar(self):
        dir_ = os.path.dirname(os.path.abspath(__file__))
        image = dir_+'\\test.png'
        f = codecs.open(image, encoding='base64')
        _file = SimpleUploadedFile(f.name, f.read())
        user = User.objects.create_user(username='user', password='122334')
        user.user_profile.avatar = _file
        user.save()
        f.close()
        self.assertEqual(user.user_profile.avatar, r"user_{0}/avatar/test.png".format(user.id))


class TestPostModel(TestCase):
    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def setUp(self):
        dir_ = os.path.dirname(os.path.abspath(__file__))
        image = dir_+'\\test.png'
        f = codecs.open(image, encoding='base64')
        self.image = SimpleUploadedFile(f.name, f.read())
        self.user = User.objects.create_user(username='user', password='122334')
        f.close()
    
    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_create_post(self):
        post = Post.objects.create(author=self.user, image=self.image)
        self.assertIsInstance(post, Post)
        self.assertRegex(str(post.image), "user_{0}/posts/test".format(self.user.id))
        self.assertEqual(post.author, self.user)

    def test_count_likes(self):
        post = Post.objects.create(author=self.user, image=self.image)
        post.likes.add(self.user)
        post.save()
        self.assertEqual(post.get_likes, 1)

