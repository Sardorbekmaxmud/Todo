from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db.models import Q

from to_do.models import ToDo


class Command(BaseCommand):
    help = "Har kuni barcha userlarning takrorlanadigan va bajarilgan todo'larini qayta faolsizlantirish"

    def handle(self, *args, **kwargs):
        today_week_num = timezone.now().weekday()

        updated_count = ToDo.objects.prefetch_related('todo_repeats').filter(
            Q(todo_repeats__repeat_day=today_week_num) &
            Q(status=True) | Q(status=False)).update(status=None)
        self.stdout.write(self.style.SUCCESS(f"{updated_count} ta todo qayta faollashtirildi."))
