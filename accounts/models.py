from django.db import models
from core.models import customUser


class accountInfo(models.Model):
    user = models.OneToOneField(customUser, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return str(self.user)

