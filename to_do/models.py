from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your models here.
class ToDo(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.CharField(max_length=250, null=True, blank=True)
    done = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __repr__(self):
        return self.body

    def __str__(self):
        return self.body


class ToDoRepeat(models.Model):
    todo = models.ForeignKey(ToDo, on_delete=models.CASCADE, related_name='todo_repeats')
    repeat_day = models.PositiveSmallIntegerField(default=None, null=True)

    def __repr__(self):
        return self.todo.body

    def __str__(self):
        return self.todo.body


class ToDoHistory(models.Model):
    todo = models.ForeignKey(ToDo, on_delete=models.CASCADE, related_name='todo_histories')
    complete_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
