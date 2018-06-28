from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.indexes import BrinIndex
from django.db import models


class User(AbstractUser):
    avatar = models.ImageField(upload_to=f'users_file', max_length=100, verbose_name='Аватар')


class Room(models.Model):
    name = models.CharField(max_length=20, unique=True, verbose_name='Комната')

    def __str__(self):
        return self.name


class Message(models.Model):
    author = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE, db_index=False)
    text = models.TextField(verbose_name='Текст')
    date = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    room = models.ForeignKey(Room, verbose_name='Комната', on_delete=models.CASCADE, db_index=False)

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        indexes = (
            BrinIndex(fields=['date']),
        )

    def __str__(self):
        return self.text

    def to_json(self):
        # print(type(self.author.avatar.url))
        return {
            'message': self.text,
            'author': self.author.username,
            'date': self.date,
            'avatar_url': self.author.avatar.url
        }

    def to_json_v2(self):
        # print(type(self.author.avatar.url))
        return {
            'message': self.text,
            'author': self.author.username,
            'date': self.date.isoformat(),
            'avatar_url': self.author.avatar.url
        }

