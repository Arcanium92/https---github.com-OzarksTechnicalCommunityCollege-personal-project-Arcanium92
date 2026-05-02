from django.urls import path
from . import views

app_name = 'game_review'

urlpatterns = [
    path('', views.home, name='home'),
    path('reviews/', views.review_list, name='review_list'),
    path('add/', views.add_review, name='add_review'),
    path('result/<int:pk>/', views.review_detail, name='review_detail'),
]
