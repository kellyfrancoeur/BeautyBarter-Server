from django.db import models
from django.contrib.auth.models import User


class Notification(models.Model):

    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_notifications', default=None)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_sent_notifications', default=None)
    viewed = models.BooleanField()
    date_created = models.DateTimeField()
    notification_type = models.ForeignKey("NotificationType", on_delete=models.CASCADE, related_name='type_notifications')

    def __str__(self):
        return self.sender.username

    def __str__(self):
        return self.receiver.username
    
    def __str__(self):
        return self.notification_type.type