from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your models here.
class ToDo(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.CharField(max_length=250, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    done = models.BooleanField(default=False)

    def __repr__(self):
        return self.body

    def __str__(self):
        return self.body
