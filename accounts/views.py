from typing import Any
from django.shortcuts import render, redirect
from django.views.generic import View
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