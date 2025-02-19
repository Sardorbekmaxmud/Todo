from django.contrib import admin
from .models import ToDo, ToDoRepeat, ToDoHistory


# Register your models here.
@admin.register(ToDo)
class ToDoAdmin(admin.ModelAdmin):
    list_display = ('author', 'body', 'created_at', 'updated_at')
    list_filter = ('created_at', 'author__username')
    search_fields = ('body', 'author__username')
    ordering = ('created_at',)
    readonly_fields = ['created_at', 'updated_at']


@admin.register(ToDoRepeat)
class ToDoRepeatAdmin(admin.ModelAdmin):
    list_display = ('todo__body', 'repeat_day')
    list_filter = ('repeat_day', 'todo__body')
    search_fields = ('todo__body',)


@admin.register(ToDoHistory)
class ToDoHistoryAdmin(admin.ModelAdmin):
    list_display = ('todo__body', 'status', 'date', 'updated_at')
    list_filter = ('date', 'status', 'todo__body')
    ordering = ('status', 'date')
    readonly_fields = ['date', 'updated_at']

    class Meta:
        db_name = 'todo_history'
        verbose_name_plural = 'todo_histories'
