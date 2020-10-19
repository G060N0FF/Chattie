from django.db import models
from django.contrib.auth import get_user_model


class Group(models.Model):
    name = models.CharField(max_length=200)
    users = models.ManyToManyField(get_user_model(), related_name='user_groups')
    code = models.CharField(max_length=10, unique=True)


class GroupMessage(models.Model):
    text = models.TextField()
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, related_name='messages')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(auto_now_add=True)
