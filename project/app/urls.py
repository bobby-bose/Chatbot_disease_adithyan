from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.RegisterUserView.as_view(), name='register'),
    path('', views.LoginUserView.as_view(), name='login'),
    path('home/', views.home, name='home'),
    path('chat/', views.chat, name='chat'),
    path('end_session/<int:session_id>/', views.end_session, name='end_session'),
]
