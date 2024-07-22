from typing import Any
from django.db.models import Q,Count,Sum
from django.db.models.functions import TruncMonth
from django.shortcuts import HttpResponseRedirect,get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
    )
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.forms import SetPasswordForm
from .forms import (
    SignUpForm,
    UserProfileForm,
    PasswordResetRequestForm,
    SellerRegisterForm,
    SellerRequestApproveForm,
    AddProductForm,
    NewProductApproveForm,
    ProductUpdateForm,
    )
from .mixins import SuperAndStaffAccessMixin,SellerAccessMixin
from .models import User,UserSellerInfo,ReportedProduct
from base.models import TheProduct,Cart,ProductHit
from django.urls import reverse_lazy,reverse
from django.views.generic import (
    CreateView,
    ListView,
    DetailView,
    UpdateView,
    DeleteView,
    View,
    )
from .base_views import BaseProductReportsView,BaseShopView
from django.contrib.auth.views import LoginView,LogoutView


#----------Authentication------------
class RegisterView(CreateView):
    form_class = SignUpForm
    template_name = 'user/register.html'

    def form_valid(self,form):
        user = form.save(commit=False)
        user.is_active = True
        user.save()
        return HttpResponseRedirect(reverse('user:login'))


class UserLoginView(LoginView):
    template_name = 'user/login.html'
    fields = '__all__'
    redirect_authenticated_user = True
    def get_success_url(self):
        return reverse_lazy('base:home')
    
class UserLogoutView(LogoutView):
    template_name = 'user/list_page.html'
    
    def get_success_url(self):
        return reverse_lazy('base:home')
    
class CustomPasswordResetView(SuccessMessageMixin, PasswordResetView):
    email_template_name = 'user/password_reset_email.html'
    template_name = 'user/password_reset.html'
    form_class = PasswordResetRequestForm
    success_url = reverse_lazy("user:password_reset_done")

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'user/password_reset_done.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'user/password_reset_confirm.html'
    form_class = SetPasswordForm
    success_url = reverse_lazy('user:password_reset_complete')

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'user/password_reset_complete.html'
    
class SellerRegisterFormView(CreateView):
    form_class = SellerRegisterForm
    template_name = 'user/seller_form.html'
    success_url = reverse_lazy('user:seller_request_detail')

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

    def get_success_url(self):
        return reverse_lazy('user:profile')
    
class AccountView(LoginRequiredMixin,UpdateView):
    form_class = UserProfileForm
    template_name = 'user/profile.html'
    success_url = reverse_lazy('user:profile')

    def get_object(self):
        return User.objects.get(pk = self.request.user.pk)
    
    def get_form_kwargs(self,**kwargs):
        kwargs = super(AccountView, self).get_form_kwargs(**kwargs)
        kwargs['user'] = self.request.user  # Pass 'user' directly to the form
        return kwargs
    
    
class PurchasedProductsView(LoginRequiredMixin,ListView):
    template_name = 'user/purchased_products.html'
    context_object_name = 'carts'

    def get_queryset(self):
        global carts
        carts = Cart.objects.filter(user=self.request.user)
        return carts
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_ids = [product.product_id for product in carts]
        products = TheProduct.objects.filter(id__in=product_ids)
        totaL_carts_price = [cart.total_cart_price for cart in carts]
        context['product'] = products
        context['total'] = sum(totaL_carts_price)
        return context

#----------Admin and staff member interface----------

class NewSellerRequestsView(SuperAndStaffAccessMixin,ListView):
    model = UserSellerInfo
    template_name = 'user/new_seller_requests.html'
    context_object_name = 'Seller_informations'

class NewSellerRequestsSearchView(SuperAndStaffAccessMixin,ListView):
    model = UserSellerInfo
    template_name = 'user/new_seller_requests.html'
    context_object_name = 'Seller_informations'

    def get_queryset(self):
        query = self.request.GET.get('SearchQuery')
        return UserSellerInfo.objects.filter(
            Q(user_id__icontains=query) |
            Q(national_code__icontains=query),
        )

class SellerRequestView(SuperAndStaffAccessMixin,UpdateView):
    #Request approve view
    form_class = SellerRequestApproveForm
    template_name = 'user/seller_request_approve.html'
    context_object_name = 'SellerRequestDetails'
    success_url = reverse_lazy('user:new_seller_requests')

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
        kwargs = super(SellerRequestView,self).get_form_kwargs()
        kwargs.update({
			'user': self.request.user
		})  
        return kwargs
    
class NewProductsView(SuperAndStaffAccessMixin,ListView):
    template_name = 'user/new_products_added.html'
    context_object_name = 'newproducts'

    def get_queryset(self):
        return TheProduct.objects.filter(availability='I')
    

class NewProductsSearchView(SuperAndStaffAccessMixin,ListView):
    '''modify the query'''
    model = TheProduct
    template_name = 'user/new_products_added.html'
    context_object_name = 'newproducts'

    def get_queryset(self):
        query = self.request.GET.get('SearchQuery')
        return TheProduct.objects.filter(
            Q(product__icontains=query) |
            Q(tags__name__icontains=query),
            availability='I'
        )

class NewProductApproveView(SuperAndStaffAccessMixin,UpdateView):
    '''Update the template'''
    template_name = 'user/new_product_added_approve.html'
    form_class = NewProductApproveForm
    context_object_name = 'product'
    success_url = reverse_lazy('user:new_products')

    def get_object(self):
        return TheProduct.objects.get(id = self.kwargs.get('id'))
    
    
class ProductReportsView(SuperAndStaffAccessMixin,BaseProductReportsView):
    queryset = ReportedProduct.objects.filter(checked=False)

class CheckedProductReportsView(SuperAndStaffAccessMixin,BaseProductReportsView):
    queryset = ReportedProduct.objects.filter(checked=True)

class ReportedProductView(SuperAndStaffAccessMixin,UpdateView):
    model = TheProduct
    fields = ['availability']
    template_name = 'user/reported_product.html'
    context_object_name = 'reportedproduct'
    success_url = reverse_lazy('user:product_reports')
    
    def get_object(self):
        global id
        id = self.kwargs.get('id')
        reportedproduct = get_object_or_404(ReportedProduct,id=id)
        reportedproduct.checked = True
        reportedproduct.save(update_fields=['checked'])
        return reportedproduct
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['product'] = TheProduct.objects.get(id=id)
        return context
    
    def form_valid(self, form):
        reported_product = self.get_object()
        the_product = reported_product.reported_product
        the_product.availability = form.cleaned_data['availability']
        the_product.save(update_fields=['availability'])
        return super().form_valid(form)

class ProductDeleteView(SuperAndStaffAccessMixin,DeleteView):
    model = TheProduct
    template_name = 'user/product_delete.html'
    context_object_name = 'product'
    success_url = reverse_lazy('user:product_reports')
    
#---------Seller interface -----------

class ShopTotalView(SellerAccessMixin,BaseShopView):

    def get_queryset(self):
        #gets the products that were created by the user
        return TheProduct.objects.filter(created_by = self.request.user.user_id)


class ShopMostViewedProductsView(SellerAccessMixin,BaseShopView):

    def get_queryset(self):
        #gets the most viewed products that were created by the user
        return TheProduct.objects.most_viewed_products(created_by = self.request.user.user_id)

class ShopMostRatedProductsView(SellerAccessMixin,BaseShopView):

    def get_queryset(self):
        #gets the most rated products that were created by the user
        return TheProduct.objects.most_rated_products(created_by = self.request.user.user_id)

class ShopNewArrivalProductsView(SellerAccessMixin,BaseShopView):

    def get_queryset(self):
        #gets the new arrival products that were created by the user
        return TheProduct.objects.new_arrivals(created_by = self.request.user.user_id)

class ShopUnavailableProductsView(SellerAccessMixin,BaseShopView):

    def get_queryset(self):
        #gets the unavailable products that were created by the user
        return TheProduct.objects.unavailables(created_by = self.request.user.user_id)
    
class ShopSearchView(SellerAccessMixin,BaseShopView):

    def get_queryset(self):
        query = self.request.GET.get('SearchQuery')
        return TheProduct.objects.filter(
            Q(product__icontains=query) |
            Q(tags__name__icontains=query),
        ).order_by('-hits').distinct()
    
class AddProductView(SellerAccessMixin,CreateView):
    form_class = AddProductForm
    template_name = 'user/add_product.html'
    success_url = reverse_lazy('user:shop')

    def form_valid(self, form):
        #automaticly insert the user_id
        form.instance.created_by = get_object_or_404(User,user_id = self.request.user.user_id)
        form.save()
        return super().form_valid(form)
    
class ProductStatsView(SellerAccessMixin,DetailView):
    model = TheProduct
    template_name = 'user/product_stats.html'

    def get_context_data(self,*args,**kwargs):
        context = super().get_context_data(**kwargs)
        product = get_object_or_404(TheProduct,pk = self.kwargs.get('pk'),created_by = self.request.user)
        carts = product.carts.filter(product=product)

        monthly_hits = ProductHit.objects.filter(product=product) \
            .annotate(month=TruncMonth('created')) \
            .values('month') \
            .annotate(hit_count=Count('id')) \
            .order_by('month')

        context['product'] = product
        context['views'] = [{"y": hit['hit_count'], "label": hit['month'].strftime('%B %Y')} for hit in monthly_hits]
        context['pending_orders'] = carts.exclude(progress_status = '100' or '00').count()
        context['shipped_orders'] = carts.filter(progress_status = '100').count()
        context['cancelled'] = carts.filter(progress_status = '00').count()
        context['earnings'] = carts.aggregate(earnings = Sum('total_cart_price')).get('earnings')
        return context
    
class ProductUpdateView(SellerAccessMixin,UpdateView):
    model = TheProduct
    form_class = ProductUpdateForm
    template_name = 'user/product_update.html'

    def get_success_url(self):
        return reverse_lazy('user:shop')




class ShippingProgressSellerView(SellerAccessMixin,ListView):
    template_name = 'user/shipping_progress_seller.html'
    context_object_name = 'carts'

    def get_queryset(self):
        global carts
        carts = Cart.objects.filter(product__created_by=self.request.user)
        return carts
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_ids = [product.product_id for product in carts]
        products = TheProduct.objects.filter(id__in=product_ids)
        totaL_carts_price = [cart.total_cart_price for cart in carts]
        context['product'] = products
        context['total'] = sum(totaL_carts_price)
        return context
    
class ShippingStatusUpdateView(SellerAccessMixin,View):

    def get(self, request, *args, **kwargs):

        cart = Cart.objects.get(id=self.kwargs.get('id'),product__created_by=self.request.user)
        
        cart.progress_status = self.kwargs.get('value')
        cart.save(update_fields=['progress_status'])

        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))