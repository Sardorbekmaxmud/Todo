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

        todo_repeat = ToDoRepeat.objects.filter(todo=todo)

        uz_weeks = {0: 'Dushanba', 1: 'Seshanba', 2: 'Chorshanba', 3: 'Payshanba', 4: 'Juma', 5: 'Shanba', 6: 'Yakshanba'}
        repeat_days = [uz_weeks[day.repeat_day] for day in todo_repeat]

        week_days = ['Dushanba', 'Seshanba', 'Chorshanba', 'Payshanba', 'Juma', 'Shanba', 'Yakshanba']
        return render(request=request,
                      template_name='todo/form.html',
                      context={'todo': todo, 'repeat_days': repeat_days, 'week_days': week_days})

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

                # if not created and todo_history.status and (timezone.now() - todo_history.updated_at) > timezone.timedelta(minutes=10):
                #     messages.error(request, "Bajarilgan vazifani 10 daqiqadan keyin bekor qilib bolmaydi.")
                #     return redirect('edit', tod.id, 'none')

                todo_history.status = False
                todo_history.save()

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

            return redirect('to_do')
