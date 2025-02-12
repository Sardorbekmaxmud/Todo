from django.contrib import admin
from .models import ToDo, ToDoRepeat


# Register your models here.
@admin.register(ToDo)
class ToDoAdmin(admin.ModelAdmin):
    list_display = ('author', 'body', 'created_at', 'done')
    list_filter = ('done', 'created_at', 'author')
    search_fields = ('body', 'author__username')
    ordering = ('created_at',)
    readonly_fields = ['created_at', 'updated_at']


@admin.register(ToDoRepeat)
class ToDoRepeatAdmin(admin.ModelAdmin):
    list_display = ('todo__body', 'repeat_day')
    list_filter = ('repeat_day',)
    search_fields = ('todo__body',)
