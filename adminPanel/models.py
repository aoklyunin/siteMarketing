import django
from django.db import models

# Create your models here.
from django.contrib.auth.models import User

# администратор, может быть создан только сис.админом
from consumer.models import Consumer


class AdminUser(models.Model):
    # пользователь
    user = models.OneToOneField(User)

