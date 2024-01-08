import requests
from decouple import config
from django.http import JsonResponse
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


class InPostPointsView(View):

    def get(self, request, *args, **kwargs):
        api_points_url = config("INPOST_ENDPOINT_SANDBOX") + "points"
        headers = {"Content-Type": "application/json",
                   "Authorization": "Bearer " + config("INPOST_TOKEN")}

        response = requests.get(api_points_url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            return JsonResponse(data)
        else:
            error_message = f"Request failed: {response.status_code}, message: {response.text}"
            return JsonResponse({"error": error_message}, status=500)
