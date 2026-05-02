from django.urls import path
from . import views

app_name = 'game_review'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('reviews/', views.review_list, name='review_list'),
    path('add/', views.add_review, name='add_review'),
    path('review/<int:pk>/', views.review_result, name='review_result'),
]