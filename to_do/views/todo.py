from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.shortcuts import render, redirect
from django.db.models import Q
from django.utils import timezone
from django.http import JsonResponse
from django.contrib import messages
import json

from to_do.models import ToDo, ToDoRepeat, ToDoHistory


class ToDoView(LoginRequiredMixin, View):
    def get(self, request):
        today_week_num = timezone.now().weekday()

        todos = (ToDo.objects.prefetch_related('todo_repeats').filter(
            Q(author=request.user) &
            (Q(todo_repeats__repeat_day=today_week_num) | Q(todo_repeats__repeat_day=None))
        ).order_by('status', 'body').values('id', 'body', 'created_at', 'status'))

        return render(request=request, template_name='todo/index.html', context={'todos': todos})

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


class ToDoActionView(LoginRequiredMixin, View):
    def post(self, request, todo_id, action=None):
        todo = ToDo.objects.filter(pk=todo_id, author=request.user).first()
        if todo:
            if action == 'done':
                todo.status = True
                todo.save()

                todo_history, created = ToDoHistory.objects.get_or_create(
                    todo=todo,
                    date=timezone.now().date()
                )
                # if not created and todo_history.status and (timezone.now() - todo_history.updated_at) > timezone.timedelta(minutes=10):
                #     messages.error(request, "Bajarilmagan vazifani 10 daqiqadan keyin bekor qilib bolmaydi.")
                #     return redirect('to_do')

                todo_history.status = True
                todo_history.save()

            elif action == 'delete':
                todo.delete()
        return redirect('to_do')


class ToDoEditView(LoginRequiredMixin, View):
    def get(self, request, todo_id, action=None):
        todo = ToDo.objects.filter(pk=todo_id, author=request.user).first()
        return render(request, template_name='todo/form.html', context={'todo': todo})

    def post(self, request, todo_id, action=None):
        if request.POST:
            body = request.POST.get('body')
            if action == 'not_done':
                todo = ToDo.objects.filter(pk=todo_id, author=request.user).first()

                todo.status = False
                todo.save()

                todo_history, created = ToDoHistory.objects.get_or_create(
                    todo=todo,
                    date=timezone.now().date()
                )

                # if not created and todo_history.status and (timezone.now() - todo_history.updated_at) > timezone.timedelta(minutes=10):
                #     messages.error(request, "Bajarilgan vazifani 10 daqiqadan keyin bekor qilib bolmaydi.")
                #     return redirect('edit', tod.id, 'none')

                todo_history.status = False
                todo_history.save()

            if body:
                ToDo.objects.filter(pk=todo_id, author=request.user).update(body=body)
            return redirect('to_do')
