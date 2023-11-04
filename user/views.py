from typing import Any
from django.shortcuts import HttpResponseRedirect,get_object_or_404
from .forms import SignupForm,UserProFileForm,SellerRegisterForm,SellerRequestApprove
from .models import User,UserSellerInfo
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
    
class SellerRegisterFormView(CreateView):
    form_class = SellerRegisterForm
    template_name = "user/sellerform.html"
    success_url = reverse_lazy("profile")

    def form_valid(self, form):
        #automaticly update the user_id
        form.instance.user_id = self.request.user.user_id
        return super().form_valid(form)
    
class NewSellerRequests(ListView):
    model = UserSellerInfo
    template_name = "user/new_seller_request.html"
    context_object_name = "Seller_informations"

class SellerRequest(UpdateView):
    form_class = SellerRequestApprove
    template_name = "user/seller_request_approve.html"
    context_object_name = "SellerRequestDetails"
    success_url = reverse_lazy("new-seller-requests")

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        # get the seller information for displaying the details
        context = super().get_context_data(**kwargs)
        user_id = self.kwargs.get('user_id')
        context['SellerInfo'] = UserSellerInfo.objects.get(user_id=user_id)
        return context
    
    def get_object(self):
        # get the user data for form
        user_id = self.kwargs.get('user_id')
        return get_object_or_404(User,user_id=user_id)
    
    def get_form_kwargs(self):
        #updates the user data
        kwargs = super(SellerRequest,self).get_form_kwargs()
        kwargs.update({
			'user': self.request.user
		})
        return kwargs

        


