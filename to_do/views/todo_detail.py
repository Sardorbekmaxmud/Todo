from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.shortcuts import render
from django.db.models import Count
from django.db.models.functions import TruncYear, TruncMonth
from django.utils import timezone
import json
import random

from to_do.models import ToDo


class ToDoDetailView(LoginRequiredMixin, View):
    def get(self, request, todo_id):
        todo = ToDo.objects.filter(pk=todo_id, author=request.user).first()

        yearly_statistics = (
            ToDo.objects.prefetch_related('todo_histories')
            .values(year=TruncYear("todo_histories__complete_date"))
            .annotate(completed=Count('*'))
            .filter(pk=todo_id, author=request.user)
            .order_by('year')
        )

        year = timezone.now().year

        monthly_statistics = (
            ToDo.objects.prefetch_related('todo_histories')
            .filter(pk=todo_id,
                    author=request.user,
                    todo_histories__complete_date__year=str(year))
            .values(month=TruncMonth("todo_histories__complete_date"))
            .annotate(completed=Count('*'))
            .order_by('month')
        )
        # print(monthly_statistics.query)

        # Yillik statistik ma'lumotlar
        try:
            yearly_data = []
            for data in yearly_statistics:
                data['year'] = data['year'].strftime('%Y')
                yearly_data.append({'year': data['year'], 'completed': data['completed'], 'pending': random.randint(1, 10)})
        except AttributeError:
            yearly_data = []

        # Oylik statistik ma’lumotlar
        uz_months = {"01": 'Yanvar', '02': 'Fevral', '03': 'Mart', '04': 'Aprel', '05': 'May', '06': 'Iyun',
                     '07': 'Iyul', '08': 'Avgust', '09': 'Sentabr', '10': 'Oktabr', '11': 'Noyabr', '12': 'Dekabr'}

        try:
            monthly_data = []
            for data in monthly_statistics:
                data['month'] = data['month'].strftime('%m')
                monthly_data.append({'month': uz_months[data['month']], 'completed': data['completed'], 'pending': random.randint(1, 10)})
        except AttributeError:
            monthly_data = []

        context = {
            "todo": todo,
            "yearly_data": json.dumps(yearly_data),
            "monthly_data": json.dumps(monthly_data)
        }

        return render(request, "todo/detail.html", context)
