from django.forms.models import BaseModelForm
from django.shortcuts import render,HttpResponseRedirect
from .forms import SignupForm,UserProFileForm
from .models import User
from django.urls import reverse_lazy
from django.views.generic import CreateView,ListView,UpdateView
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
    
class AccountView(UpdateView):
    model = User
    form_class = UserProFileForm
    template_name = "user/profile.html"
    success_url = reverse_lazy("profile")

    def get_object(self):
        return User.objects.get(pk= self.request.user.pk)
    
    def get_form_kwargs(self):
        kwargs = super(AccountView,self).get_form_kwargs()
        kwargs.update({
			'user': self.request.user
		})
        return kwargs

