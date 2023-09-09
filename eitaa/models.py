from django.db import models


class Users(models.Model):
    user_id = models.IntegerField()
    token = models.CharField(max_length=50, null=True)


class Channels(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    channel = models.CharField(max_length=20)
