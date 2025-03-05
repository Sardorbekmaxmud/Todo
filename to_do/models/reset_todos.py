from django.db import models


class ResetTodos(models.Model):
    date = models.DateField()

    class Meta:
        verbose_name_plural = 'reset_todos'
