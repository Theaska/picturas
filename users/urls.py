from django.contrib import admin
from django.urls import path, include
from users.views import *
from django.contrib.auth import views 

app_name = 'users'
urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/<int:user_id>', ProfileView.as_view(), name='profile'),
    path('profile/<int:user_id>/add_remove_friend', login_required(AddRemoveFriend.as_view()), name='add-remove-friend'),
    path('profile/<int:user_id>/edit', login_required(EditProfileView.as_view()), name='edit-profile'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('password_reset/', views.PasswordResetView.as_view(success_url=reverse_lazy('users:password_reset_done'), template_name='registration/password_reset.html'), name='password_reset'),
    path('password_reset/done', views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('password_reset/<str:uidb64>/<slug:token>', views.PasswordResetConfirmView.as_view(success_url=reverse_lazy('users:password_reset_complete')), name='password_reset_confirm'),
    path('password_reset/complete', views.PasswordResetCompleteView.as_view(), name='password_reset_complete')
]
