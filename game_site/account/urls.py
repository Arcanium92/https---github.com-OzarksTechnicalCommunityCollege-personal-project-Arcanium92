from django.urls import path
from django.contrib.auth import views as auth_views

app_name = 'account'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
]