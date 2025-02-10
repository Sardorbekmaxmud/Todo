from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm
from django.views import generic
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from .models import ToDo
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.
def login_required_decorator(func):
    return login_required(function=func, login_url='login')


class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/sign_up.html'


@login_required_decorator
def logout_(reqeust):
    logout(request=reqeust)

    return redirect('login')


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
