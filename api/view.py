from rest_framework import viewsets
from models.models import Chat
from .serializer import ChatSerializer
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework.response import Response

class ChatView(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('chat',) 

    def retrieve(self, request, pk=None):
        queryset = Chat.objects.all()
        chat = get_object_or_404(queryset, chat=pk)
        serializer = ChatSerializer(chat)
        return Response(serializer.data)
    
    def partial_update(self, request, *args, **kwargs):
        try:
            # находим объект с указанным значением поля chat
            instance = Chat.objects.get(chat=int(request.data.get('chat')))
            
            # создаем обновленный словарь с нужным полем
            updated_data = {'level': request.data.get('level')}
            
            serializer = self.get_serializer(
                instance,
                data=updated_data,
                partial=True  # разрешаете частичное обновление
            )
            
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=400)
        except Chat.DoesNotExist:
            return Response({"detail": f"Объект с chat={request.data.get('chat')} не существует."}, status=404)