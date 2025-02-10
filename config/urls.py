from django.contrib import admin
from django.urls import path, include
from to_do.views import SignUpView, logout_
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_, name='logout'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('', include("to_do.urls")),
]
