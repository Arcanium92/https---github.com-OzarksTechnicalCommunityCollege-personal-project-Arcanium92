from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('reviews/', views.review_list, name='review_list'),
    path('reviews/add/', views.add_review, name='add_review'),
    path('reviews/<int:pk>/result/', views.review_result, name='review_result'),
    path('reviews/<int:review_id>/', views.review_detail, name='review_detail'),
    path('reviews/<int:review_id>/like/', views.toggle_like, name='toggle_like'),
    path('pokemon/random/', views.random_pokemon, name='random_pokemon'),
]