from typing import Any
from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from . import forms

# Create your views here.

class Register(View):
    def setup(self, request, *args: Any, **kwargs: Any):
        self.form_class = forms.RegisterForm
        return super().setup(request, *args, **kwargs)
    def get(self, request):
        form = self.form_class()
        return render(request, "accounts/register.html", {"form": form})
    
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect("accounts:login")
        else:
            print("hello world")
            return render(request, "accounts/register.html", {"form": form})

class Login(LoginView):
    template_name = "accounts/login.html"
    success_url = "dashboard:home"

class Logout(View):
    def get(self, request):
        logout(request)
        return redirect("landing:home")
