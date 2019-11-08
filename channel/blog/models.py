from django.db import models

class Message(models.Model):
    
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    status = models.BooleanField(default=True)
    date_add = models.DateTimeField(auto_now_add=True)
    date_upd = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.message
        