from django.db import models


# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=200)
    email = models.CharField(max_length=100,default='student@126.com')
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'user'
