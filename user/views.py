from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import HttpResponseRedirect,get_object_or_404
from .forms import (
    SignupForm,
    UserProFileForm,
    SellerRegisterForm,
    SellerRequestApprove,
    )
from .models import User,UserSellerInfo
from base.models import TheProduct
from django.urls import reverse_lazy,reverse
from django.views.generic import CreateView,ListView,UpdateView,DetailView
from django.contrib.auth.views import LoginView

#----------Form views-----------

class Register(CreateView):
    form_class = SignupForm
    template_name = "user/register.html"

    def form_valid(self,form):
        user = form.save(commit=False)
        user.is_active = True
        user.save()
        return HttpResponseRedirect(reverse('user:profile'))


class UserLogin(LoginView):
    template_name = 'user/login.html'
    fields = '__all__'
    redirect_authenticated_user = True
    def get_success_url(self):
        return reverse_lazy('base:home')
    
class SellerRegisterFormView(CreateView):
    form_class = SellerRegisterForm
    template_name = "user/sellerform.html"
    success_url = reverse_lazy("user:seller-request-detail")

    def form_valid(self, form):
        # Use the user_id as global
        global user_id
        user_id = self.request.user.user_id
        #automaticly update the user_id
        form.instance.user_id = user_id
        return super().form_valid(form)

    def post(self, request):
        # Get the model
        instance = get_object_or_404(User, pk=request.user.pk)

        # Update the is_seller status to Investigate
        instance.is_seller = 'I'
        instance.save()
        return super().post(self)

    def get_success_url(self) -> str:
        return reverse_lazy("user:seller-request-detail",kwargs={'user_id': user_id})

class NewSellerRequests(ListView):
    model = UserSellerInfo
    template_name = "user/new_seller_request.html"
    context_object_name = "Seller_informations"

class SellerRequest(UpdateView):
    form_class = SellerRequestApprove
    template_name = "user/seller_request_approve.html"
    context_object_name = "SellerRequestDetails"
    success_url = reverse_lazy("user:new-seller-requests")

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

#---------User account interface -----------

class AccountView(UpdateView):
    model = User
    form_class = UserProFileForm
    template_name = "user/profile.html"
    success_url = reverse_lazy("user:profile")

    def get_object(self):
        return User.objects.get(pk= self.request.user.pk)
    
    def get_form_kwargs(self):
        kwargs = super(AccountView,self).get_form_kwargs()
        kwargs.update({
			'user': self.request.user
		})
        return kwargs
    
    def form_valid(self, form):
        profile = form.save()
        user = profile.user
        user.save()

class ShopTotalView(ListView):
    template_name = "user/shop.html"
    context_object_name = "created_products"

    def get_queryset(self):
        #gets the products that were created by the user
        return TheProduct.objects.filter(created_by = self.request.user.user_id)


class ShopMostViewedProductsView(ListView):
    template_name = "user/shop.html"
    context_object_name = "created_products"

    def get_queryset(self):
        #gets the most viewed products that were created by the user
        return TheProduct.objects.mostviewedproducts(created_by = self.request.user.user_id)

class ShopMostRatedProductsView(ListView):
    template_name = "user/shop.html"
    context_object_name = "created_products"

    def get_queryset(self):
        #gets the most rated products that were created by the user
        return TheProduct.objects.mostratedproducts(created_by = self.request.user.user_id)

class ShopNewArrivalProductsView(ListView):
    template_name = "user/shop.html"
    context_object_name = "created_products"

    def get_queryset(self):
        #gets the new arrival products that were created by the user
        return TheProduct.objects.newarrivals(created_by = self.request.user.user_id)

class ShopUnavailableProductsView(ListView):
    template_name = "user/shop.html"
    context_object_name = "created_products"

    def get_queryset(self):
        #gets the unavailable products that were created by the user
        return TheProduct.objects.unavailables(created_by = self.request.user.user_id)


