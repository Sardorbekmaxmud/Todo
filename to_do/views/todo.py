from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.utils import timezone
from django.http import JsonResponse
import json

from to_do.models import ToDo, ToDoRepeat, ToDoHistory


class ToDoView(LoginRequiredMixin, View):
    def get(self, request):
        today_week_num = timezone.now().weekday()

        todos = (ToDo.objects.prefetch_related('todo_repeats').filter(
            Q(author=request.user) &
            (Q(todo_repeats__repeat_day=today_week_num) | Q(todo_repeats__repeat_day=None))
        ).order_by('done', 'body'))

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
    def post(self, request, todo_id, action):
        todo = ToDo.objects.filter(pk=todo_id, author=request.user).first()
        if todo:
            if action == 'done':
                todo.done = True
                ToDoHistory.objects.create(todo=todo)

                todo.save()
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
                ToDo.objects.filter(pk=todo_id, author=request.user).update(done=False)
            if body:
                ToDo.objects.filter(pk=todo_id, author=request.user).update(body=body)
            return redirect('to_do')


class ToDoDetailView(LoginRequiredMixin, View):
    def get(self, request, todo_id):
        todo = ToDo.objects.filter(pk=todo_id, author=request.user).first()

        # Yillik statistik ma’lumotlar
        yearly_data = [
            {"year": 2023, "completed": 45, "pending": 20},
            {"year": 2024, "completed": 50, "pending": 30},
            {"year": 2025, "completed": 70, "pending": 25}
        ]

        # Oylik statistik ma’lumotlar
        monthly_data = [
            {"month": "Yanvar", "completed": 5, "pending": 2},
            {"month": "Fevral", "completed": 8, "pending": 4},
            {"month": "Mart", "completed": 12, "pending": 6},
            {"month": "Aprel", "completed": 15, "pending": 7},
            {"month": "May", "completed": 10, "pending": 5},
            {"month": "Iyun", "completed": 20, "pending": 8},
            {"month": "Iyul", "completed": 18, "pending": 10},
            {"month": "Avgust", "completed": 22, "pending": 12},
            {"month": "Sentabr", "completed": 19, "pending": 11},
            {"month": "Oktabr", "completed": 17, "pending": 9},
            {"month": "Noyabr", "completed": 25, "pending": 10},
            {"month": "Dekabr", "completed": 30, "pending": 15}
        ]

        context = {
            "todo": todo,
            "yearly_data": json.dumps(yearly_data),
            "monthly_data": json.dumps(monthly_data)
        }

        return render(request, "todo/detail.html", context)
