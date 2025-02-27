from django.db.models import Q
from django.utils.timezone import now
from django.core.cache import cache

from to_do.models import ToDo


class ResetTodosMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        today = now().date()
        last_reset = cache.get("last_todos_reset")

        if last_reset is None or last_reset < today:
            today_week_num = now().weekday()

            ToDo.objects.prefetch_related('todo_repeats').filter(
                Q(todo_repeats__repeat_day=today_week_num) &
                Q(status=True) | Q(status=False)).update(status=None)
            cache.set("last_todos_reset", today, timeout=86400)  # 24 soat cache

        response = self.get_response(request)
        return response
