from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
# Обьявление обычного роутера
router = DefaultRouter()

# Создание CRUD операций для набора представлений snippets
router.register(r'snippets', views.SnippetViewSet)
# Создание CRUD операций для набора представлений user
router.register(r'users', views.UserViewSet)

urlpatterns = [
    # Перекидываем пустой путь на пути роутера.
    path('', include(router.urls)),
]
