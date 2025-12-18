from django.db import models

class Chat(models.Model):
    chat = models.IntegerField(unique=True)
    name = models.CharField(max_length=30,default='name')
    level = models.IntegerField(default=1) 