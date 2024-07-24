from django.http import Http404,HttpResponseForbidden
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404,redirect
from django import forms
#Access mixins
class SuperAndStaffAccessMixin():
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser or request.user.is_staff:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404("You don't have access to this page")
        
class SellerAccessMixin():
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_seller == 'A' or request.user.is_superuser :
            return super().dispatch(request, *args, **kwargs)
        else:
            #create a custom template later
            raise PermissionDenied("You must be a seller access to this page")
        
class SpecsJsonFieldValidationMixin():
    def clean_specs(self):
        specs = self.cleaned_specs.get('specs')
        if not isinstance(specs, dict):
            raise forms.ValidationError("Invalid JSON: Please enter a valid JSON object.")
        return specs
