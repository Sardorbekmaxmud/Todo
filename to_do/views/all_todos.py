from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic

from to_do.models import ToDo


class AllToDosView(LoginRequiredMixin, generic.ListView):
    context_object_name = 'all_todos'
    paginate_by = 7
    template_name = 'todo/all_todos.html'

    def get_queryset(self):
        return ToDo.objects.filter(author=self.request.user).order_by('-created_at')
