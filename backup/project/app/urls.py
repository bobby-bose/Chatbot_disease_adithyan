from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('home/', views.home, name='home'),
    path('chat/', views.chat, name='chat'),
    path('end_session/<int:session_id>/', views.end_session, name='end_session'),
]
