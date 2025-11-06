from django.contrib.auth.models import User
from rest_framework import viewsets, permissions, renderers
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Snippet
from .serializers import SnippetSerializer, UserSerializer
from .permissions import IsOwnerOrReadOnly

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    # Выборка всех юзеров и их сериализация
    queryset = User.objects.all()
    serializer_class = UserSerializer


class SnippetViewSet(viewsets.ModelViewSet):

    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    #Проверка на авторизацию и права измененния Снипетта
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]
    #Действие для аодсветки и генерация отдельной страницы с цветным кодом
    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

    #Сохраняем пользователя создавшего сниппет как создателя в поле owner
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
