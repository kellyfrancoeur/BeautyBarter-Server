from django.db import models
from django.contrib.auth.models import User


class Message(models.Model):

    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender_user_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipient_user_messages')
    date_time = models.DateTimeField()
    content = models.TextField(blank=True)

    def __str__(self):
        return self.sender.username

    def __str__(self):
        return self.recipient.username