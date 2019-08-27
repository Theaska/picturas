from django.contrib import admin
from django.contrib.auth.models import User
from blog.models import Post
from django.contrib.auth.admin import UserAdmin 
from users.models import Profile

class PostInline(admin.StackedInline):
    model = Post
    extra = 3

admin.site.unregister(User)

@admin.register(User)
class UserAdmin(UserAdmin):
    inlines = [PostInline]

admin.site.register(Post)
admin.site.register(Profile)