
from rest_framework.permissions import AllowAny
from rest_framework import viewsets, mixins
from django.contrib.auth.models import User
from .models import News
from .serializers import NewsSerializer, UserSerializer
from .permissions import IsAuthorOrReadOnly

class UserViewSet(viewsets.ModelViewSet):
    """
    API для управления пользователями (регистрация, просмотр).
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny] # <--- ВОТ ЭТА СТРОКА
    http_method_names = ['get', 'post', 'head', 'options']

class NewsViewSet(viewsets.ModelViewSet):
    """
    API для управления новостями (CRUD).
    """
    queryset = News.objects.all().order_by('-date_created')
    serializer_class = NewsSerializer
    permission_classes = [IsAuthorOrReadOnly]
    # Фильтрация по автору: /api/news/?author=5
    filterset_fields = ['author']
    # Поиск по заголовку: /api/news/?search=текст
    search_fields = ['title', 'summary']

    def perform_create(self, serializer):
        # Автоматически назначаем автора текущим пользователем
        serializer.save(author=self.request.user)
