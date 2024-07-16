from user.models import User
from base.models import Cart
from base.models import PagePic

class PageDataMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add the background_pic to the context
        context['background_pic'] = PagePic.objects.get().website_pic

        if self.request.user.is_authenticated:
            context['user_profile'] = User.objects.get(pk=self.request.user.pk).profile
            context['username'] = User.objects.get(pk=self.request.user.pk).username
            context['cart'] = Cart.objects.filter(user=self.request.user,checkout=False)
            context['quantity'] = context['cart'].count()
        return context