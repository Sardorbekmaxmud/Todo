from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.views import View
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.db.models import Q
from django.utils import timezone
from django.http import JsonResponse
import json

from .models import ToDo, ToDoRepeat
from .forms import CustomUserCreationForm


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
        today_week_num = timezone.now().weekday()

        todos = (ToDo.objects.prefetch_related('todorepeat_set').filter(
            Q(author=request.user) &
            (Q(todorepeat__repeat_day=today_week_num) | Q(todorepeat__repeat_day=None))
        ).order_by('-created_at', ))

        return render(request=request, template_name='to_do.html', context={'todos': todos})

    def post(self, request):
        try:
            data = json.loads(request.body)

            body = data.get('body', '').strip()
            if not body:
                return JsonResponse({"error": "Vazifa nomi bo‘lishi shart!"}, status=400)
            todo = ToDo.objects.create(author=request.user, body=body)

            # Tanlangan haftalik kunlar uchun `ToDoRepeat` obyektlari yaratish
            repeat_days = data.get('repeat_days', [])
            if not isinstance(repeat_days, list):
                return JsonResponse({"error": "repeat_days ro'yxat ko'rinishida bo'lishi kerak!"}, status=400)

            if repeat_days:
                ToDoRepeat.objects.bulk_create([
                    ToDoRepeat(todo=todo, repeat_day=day) for day in repeat_days
                ])

            return JsonResponse({'success': True}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)

        # body = request.POST.get('body')
        # if body:
        #     ToDo.objects.create(
        #         author=request.user,
        #         body=body
        #     )
        # return redirect('to_do')


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
