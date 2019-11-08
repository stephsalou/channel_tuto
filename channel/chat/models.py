from django.db import models

# Create your models here.
class Message(models.Model):
    message = models.TextField()
    status = models.BooleanField(default=True)
    date_add = models.DateTimeField(auto_now_add=True)
    date_upd = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.message

    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'