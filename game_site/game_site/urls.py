from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('game_review.urls', namespace='game_review')),
    path('account/', include('account.urls', namespace='account')),
]
