from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Маршруты веб-интерфейса (Лаба 2)
    path('', include('news_app.urls')),
    # Маршруты API (Лаба 3)
    path('api/', include('news_app.api_urls')),
]
