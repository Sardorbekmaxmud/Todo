from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views import View
from django.shortcuts import render, redirect
from django.db.models import Q
from django.utils import timezone
import json

from to_do.models import ToDo, ToDoRepeat


class ToDoTodayView(LoginRequiredMixin, View):
    def get(self, request):
        today_week_num = timezone.now().weekday()

        todos = (ToDo.objects.prefetch_related('todo_repeats').filter(
            Q(author=request.user) &
            (Q(todo_repeats__repeat_day=today_week_num) | Q(todo_repeats__repeat_day=None))
        ).order_by('-status').values('id', 'body', 'created_at', 'status'))

        return render(request=request,
                      template_name='todo/index.html',
                      context={'todos': todos})

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

            return redirect('to_do')

        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
