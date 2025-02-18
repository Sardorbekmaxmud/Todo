from django.urls import path
from .views import ToDoView, ToDoActionView, ToDoEditView, ToDoDetailView


urlpatterns = [
    path('', ToDoView.as_view(), name='to_do'),
    path('todo/<int:todo_id>/<str:action>/action/', ToDoActionView.as_view(), name='action'),
    path('todo/<int:todo_id>/<str:action>/edit/', ToDoEditView.as_view(), name='edit'),
    path('todo/detail/<int:todo_id>/', ToDoDetailView.as_view(), name='todo_detail'),
]
