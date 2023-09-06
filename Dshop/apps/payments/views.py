from django.views.generic.base import TemplateView


class PurchaseView(TemplateView):
    template_name = 'payments/purchase.html'
