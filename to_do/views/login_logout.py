from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.shortcuts import redirect
from django.urls import reverse_lazy
from to_do.forms import CustomUserCreationForm


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
