from django.contrib import admin
from .models import ToDo, ToDoRepeat, ToDoHistory


# Register your models here.
@admin.register(ToDo)
class ToDoAdmin(admin.ModelAdmin):
    list_display = ('author', 'body', 'done', 'created_at', 'updated_at')
    list_filter = ('created_at', 'author__username', 'done')
    search_fields = ('body', 'author__username')
    ordering = ('created_at',)
    readonly_fields = ['created_at', 'updated_at']


@admin.register(ToDoRepeat)
class ToDoRepeatAdmin(admin.ModelAdmin):
    list_display = ('todo__body', 'repeat_day')
    list_filter = ('repeat_day',)
    search_fields = ('todo__body',)


@admin.register(ToDoHistory)
class ToDoHistoryAdmin(admin.ModelAdmin):
    list_display = ('todo__body', 'complete_date', 'updated_at')
    list_filter = ('complete_date',)
    ordering = ('complete_date', 'updated_at')
    readonly_fields = ['complete_date', 'updated_at']

    class Meta:
        db_name = 'todo_history'
        verbose_name_plural = 'todo_histories'
