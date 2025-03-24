from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.shortcuts import render


class ToDoCreateView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request=request, template_name='todo/create_todo.html', status=200)
