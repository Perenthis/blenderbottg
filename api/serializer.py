
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from models.models import Chat

class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ('__all__')