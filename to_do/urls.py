from django.urls import path
from .views import (ToDoTodayView, ToDoActionView,
                    ToDoEditView, ToDoDetailView,
                    AllToDosView, ToDoCreateView)

urlpatterns = [
    path('', ToDoTodayView.as_view(), name='to_do'),
    path('todos/', AllToDosView.as_view(), name='all_todos'),
    path('todo/create/', ToDoCreateView.as_view(), name='create'),
    path('todo/<int:todo_id>/<str:action>/action/', ToDoActionView.as_view(), name='action'),
    path('todo/<int:todo_id>/<str:action>/edit/', ToDoEditView.as_view(), name='edit'),
    path('todo/detail/<int:todo_id>/', ToDoDetailView.as_view(), name='todo_detail'),
]
