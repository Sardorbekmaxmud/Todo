from django.urls import path
from .views import ToDoView, ToDoActionView, ToDoEditView


urlpatterns = [
    path('', ToDoView.as_view(), name='to_do'),
    path('<int:todo_id>/<str:action>/action/', ToDoActionView.as_view(), name='action'),
    path('<int:todo_id>/<str:action>/edit/', ToDoEditView.as_view(), name='edit'),
]
