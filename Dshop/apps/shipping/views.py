import requests
from django.http import JsonResponse
from django.views import View


class InPostSendingMethodsView(View):
    def get(self, request, *args, **kwargs):
        api_url = "https://api-shipx-pl.easypack24.net/v1/sending_methods"

        headers = {
            "Content-Type": "application/json",
        }

        response = requests.get(api_url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            return JsonResponse(data, safe=False)
        else:

            return JsonResponse({'error': f'Request failed: {response.status_code}, '
                                          f'message: {response.text}'}, status=500)
