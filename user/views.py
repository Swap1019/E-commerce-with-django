from django.shortcuts import render,HttpResponseRedirect
from .forms import SignupForm
from django.urls import reverse_lazy
from django.views.generic import CreateView

class Register(CreateView):
    form_class = SignupForm
    template_name = "user/register.html"

    def form_valid(self,form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        return HttpResponseRedirect("")