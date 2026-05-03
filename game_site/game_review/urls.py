from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('add/', views.add_review, name='add_review'),
    path('reviews/', views.review_list, name='review_list'),
    path('reviews/<int:pk>/', views.review_result, name='review_result'),
    path("pokemon/random/", views.random_pokemon, name="random_pokemon"),
]