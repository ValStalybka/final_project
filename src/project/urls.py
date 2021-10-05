from django.contrib import admin
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.urls import include
from django.urls import path
from django.views.generic.base import RedirectView
from django.shortcuts import redirect



urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("applications.blog.urls"), name="blog"),
    path("", include("applications.registration.urls"), name="registration"),
]
