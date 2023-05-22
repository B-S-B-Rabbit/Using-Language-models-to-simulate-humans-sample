"""
This module defines the URequest model used for handling user requests.

"""

from django.db import models
from django.contrib.auth.models import User


class URequest(models.Model):
    """
    Model for handling user requests.

    Attributes:
        user (ForeignKey): The user who made the request.
        request_text (TextField): The text of the request.
        request_date (DateTimeField): The date and time when the request was made.
        response_text (TextField): The text of the response (can be blank and null).

    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    request_text = models.TextField()
    request_date = models.DateTimeField(auto_now_add=True)
    response_text = models.TextField(blank=True, null=True)

    objects = models.Manager()

    def __str__(self):
        """
        Returns a string representation of the request text.

        Returns:
            str: The request text.

        """
        return self.request_text
