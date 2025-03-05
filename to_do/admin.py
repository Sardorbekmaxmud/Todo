from django.contrib import admin
from .models import ToDo, ToDoRepeat, ToDoHistory, ResetTodos


# Register your models here.
@admin.register(ToDo)
class ToDoAdmin(admin.ModelAdmin):
    list_display = ('author', 'body', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'created_at', 'author__username')
    search_fields = ('body', 'author__username')
    ordering = ('status', 'created_at')
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
    ordering = ('date',)
    readonly_fields = ['date', 'updated_at']


@admin.register(ResetTodos)
class ResetTodosAdmin(admin.ModelAdmin):
    list_display = ('date',)
    list_filter = ('date',)
    readonly_fields = ['date',]
