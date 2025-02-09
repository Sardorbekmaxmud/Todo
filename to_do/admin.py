from django.contrib import admin
from .models import ToDo


# Register your models here.
@admin.register(ToDo)
class ToDoAdmin(admin.ModelAdmin):
    list_display = ('author', 'body', 'created_at', 'done')
    list_filter = ('done', 'created_at', 'author')
    search_fields = ('body', 'author__username')
    ordering = ('created_at',)
    readonly_fields = ['created_at']
