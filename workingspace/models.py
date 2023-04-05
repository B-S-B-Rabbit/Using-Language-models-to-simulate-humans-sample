from django.db import models
from django.contrib.auth.models import User


class URequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    request_text = models.TextField()
    request_date = models.DateTimeField(auto_now_add=True)
    response_text = models.TextField(blank=True, null=True)

    objects = models.Manager()

    def __str__(self):
        return self.request_text