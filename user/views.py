from django.shortcuts import render,HttpResponseRedirect
from .forms import SignupForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView,LogoutView

class Register(CreateView):
    form_class = SignupForm
    template_name = "user/register.html"

    def form_valid(self,form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        return HttpResponseRedirect("")


class UserLogin(LoginView):
    template_name = 'user/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('base:home')
    
class UserLogout(LogoutView):

    def get_success_url(self):
        return reverse_lazy('base:home')