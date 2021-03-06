from django.db import models
from django.contrib.auth.models import User
# Create your models here.

# choices tuple having (value, label) pair
LANGUAGE_CHOICES = [('C++', 'C SHARP'), ('PY', 'PYTHON'), ('JS', 'JAVASCRIPT'), ('J', 'JAVA')]


class Question(models.Model):
    title = models.CharField(max_length=100)
    name = models.CharField(max_length=20)
    user = models.ForeignKey(User, related_name='questioner', on_delete=models.CASCADE, default=1)
    language = models.CharField(max_length=5, choices=LANGUAGE_CHOICES, default='PYTHON')
    phone = models.IntegerField(null=True)
    address = models.TextField()

    def __str__(self):
        return self.title

