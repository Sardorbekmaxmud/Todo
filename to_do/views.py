from django.shortcuts import render, reverse, redirect
from .models import ToDo
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View


# Create your views here.
class ToDoView(LoginRequiredMixin, View):
    def get(self, request):
        todos = ToDo.objects.filter(author=request.user).order_by('-created_at',)
        return render(request=request, template_name='to_do.html', context={'todos': todos})

    def post(self, request):
        body = request.POST.get('body')
        if body:
            ToDo.objects.create(
                author=request.user,
                body=body
            )
        return redirect('to_do')


class ToDoActionView(LoginRequiredMixin, View):
    def post(self, request, todo_id, action):
        todo = ToDo.objects.filter(pk=todo_id, author=request.user).first()
        if todo:
            if action == 'done':
                todo.done = True
                todo.save()
            elif action == 'delete':
                todo.delete()
        return redirect('to_do')


class ToDoEditView(LoginRequiredMixin, View):
    def get(self, request, todo_id, action=None):
        todo = ToDo.objects.filter(pk=todo_id, author=request.user).first()
        return render(request, template_name='form.html', context={'todo': todo})

    def post(self, request, todo_id, action=None):
        if request.POST:
            body = request.POST.get('body')
            if action == 'not_done':
                ToDo.objects.filter(pk=todo_id, author=request.user).update(done=False)
            if body:
                ToDo.objects.filter(pk=todo_id, author=request.user).update(body=body)
            return redirect('to_do')
