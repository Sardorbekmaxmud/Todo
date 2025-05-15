from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views import View
from django.contrib import messages

from to_do.models import ToDo, ToDoHistory, ToDoRepeat


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

                todo_history.status = True
                todo_history.save()

                return redirect('to_do')

            elif action == 'delete':
                todo.delete()
        return redirect('all_todos')


class ToDoEditView(LoginRequiredMixin, View):

    def get(self, request, todo_id, action=None):
        todo = ToDo.objects.get(pk=todo_id, author=request.user)
        existing_days = todo.todo_repeats.values_list('repeat_day', flat=True)
        uz_weeks = {0: 'Dushanba', 1: 'Seshanba', 2: 'Chorshanba', 3: 'Payshanba', 4: 'Juma', 5: 'Shanba',
                    6: 'Yakshanba'}
        inv_uz_weeks = {v: k for k, v in uz_weeks.items()}

        # Translate numeric repeat days back to Uzbek names
        repeat_days = [day for day in uz_weeks.values() if inv_uz_weeks[day] in existing_days]

        context = {
            'todo': todo,
            'week_days': list(uz_weeks.values()),
            'repeat_days': repeat_days  # Har doim list bo'ladi, bo'sh bo'lsa ham
        }

        return render(request=request,
                      template_name='todo/form.html',
                      context=context,
         )

    def post(self, request, todo_id, action=None):
        if request.POST:
            body = request.POST.get('body')
            repeat_days = request.POST.getlist('repeat_days[]', [])
            uz_weeks = {'Dushanba': 0, 'Seshanba': 1, 'Chorshanba': 2, 'Payshanba': 3, 'Juma': 4, 'Shanba': 5,
                        'Yakshanba': 6}

            if action == 'not_done':
                todo = ToDo.objects.filter(pk=todo_id, author=request.user).first()

                todo.status = False
                todo.save()

                todo_history, created = ToDoHistory.objects.get_or_create(
                    todo=todo,
                    date=timezone.now().date()
                )

                todo_history.status = False
                todo_history.save()

                return redirect('to_do')

            if body:
                ToDo.objects.filter(pk=todo_id, author=request.user).update(body=body)

            if repeat_days:
                # Change repeat days to week day numbers
                num_repeat_days = [uz_weeks[day] for day in repeat_days]

                # Delete all repeat days of T0D0
                todo = ToDo.objects.filter(pk=todo_id, author=request.user).first()
                todo.todo_repeats.all().delete()

                ToDoRepeat.objects.bulk_create([
                    ToDoRepeat(todo=todo, repeat_day=day) for day in num_repeat_days
                ])
            else:
                # Agar hech qanday kun tanlanmagan bo‘lsa, eski repeat_day'larni o‘chir
                todo = ToDo.objects.filter(pk=todo_id, author=request.user).first()
                todo.todo_repeats.all().delete()

            return redirect('all_todos')
