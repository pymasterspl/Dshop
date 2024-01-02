import os

import requests
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View


class InPostSendingMethodView(View):

    def get(self, request, *args, **kwargs):
        api_url = "https://api-shipx-pl.easypack24.net/v1/sending_methods"
        headers = {"Content-Type": "application/json"}

        response = requests.get(api_url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            return JsonResponse(data)
        else:
            error_message = f"Request failed: {response.status_code}, message: {response.text}"
            return JsonResponse({"error": error_message}, status=500)


class InPostShippingView(View):
    template_name = 'shipping/shipping_form.html'

    def get(self, request, *args, **kwargs):
        context = {
            "token_for_geo": os.getenv('INPOST_GEOWIDGET_TOKEN'),
            "language": "pl",
        }

        return render(request, self.template_name, context)


class PaczkomatPageView(View):
    template_name = 'shipping/geowidget.html'

    def get(self, request, *args, **kwargs):
        context = {
            'token_for_geo': os.getenv('INPOST_GEOWIDGET_TOKEN'),
            'language': 'pl',
        }

        return render(request, self.template_name, context)


class HandleMethodChoiceView(View):
    template_name = 'shipping/handle_shipping_method.html'

    def post(self, request, *args, **kwargs):
        selected_method_id = request.POST.get('selected_method')
        customer_name = request.POST.get('name')
        address = request.POST.get('street')
        city = request.POST.get('city')
        postal = request.POST.get('postal')
        info = request.POST.get('info')
        return render(request, self.template_name, {"selected_method_id": selected_method_id, "name": customer_name,
                                                    "city": city, "address": address, "postal": postal, "info": info})
