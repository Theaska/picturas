from django.contrib import admin
from django.urls import path, include
from blog.views import *
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

app_name = 'picturas'
urlpatterns = [
    path('post/<int:post_id>', PostView.as_view(), name='post'),
    path('post/<int:post_id>/like', login_required(LikePostView.as_view()), name='like-post'),
    path('post/<int:post_id>/edit', login_required(EditPostView.as_view()), name='edit-post'),
    path('post/<int:post_id>/delete', login_required(DeletePostView.as_view()), name='delete-post'),
    path('post/<int:post_id>/delete_success', TemplateView.as_view(template_name='blog/delete_success.html'), name='delete-post-success'),
    path('', IndexView.as_view(), name='index'),
    path('feed/', FeedView.as_view(), name='feed'),
    path('create_post/', CreatePostView.as_view(), name='create-post')
]
