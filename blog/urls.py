# blog/urls.py
from django.urls import path
from .views import post_detail, add_post, home, register, edit_comment, profile, post_list
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('post/<int:post_id>/', post_detail, name='post_detail'),
    path('', home, name='home'),
    path('register/', register, name='register'),
    path('comment/<int:comment_id>/edit/', edit_comment, name='edit_comment'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', profile, name='profile'),
    path('postlist', post_list, name='post_list'),
    path('add/', add_post, name='add_post'),




]
