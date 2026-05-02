from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # Authentication
    path('account/', include('account.urls', namespace='account')),

    # Main website
    path('', include('game_review.urls', namespace='game_review')),
]