from django.db import models
from django.contrib.auth import get_user_model


class GroupMessage(models.Model):
    group_name = models.CharField(max_length=200)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True)
