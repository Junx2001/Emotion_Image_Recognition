from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('home/', views.home_view, name='home'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('profile/<int:user_id>/', views.user_profile_view, name='user_profile'),
    path('upload/', views.upload_file, name='upload'),
    path('my-albums/<str:emotion>/', views.my_album_view, name='my_album'),
    path('upload-multiples/', views.upload_images, name='upload_images'),
]