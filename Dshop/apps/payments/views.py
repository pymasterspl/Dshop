import stripe
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.http.response import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView


class PurchaseView(TemplateView):
    template_name = 'payments/purchase.html'


@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)


@csrf_exempt
def create_checkout_session(request):
    if request.method == 'GET':
        stripe.api_key = settings.STRIPE_SECRET_KEY
        product_price = 99.99
        try:
            current_site = get_current_site(request)
            domain = current_site.domain
            protocol = 'https' if request.is_secure() else 'http'
            checkout_session = stripe.checkout.Session.create(
                client_reference_id=request.user.id if request.user.is_authenticated else None,
                success_url=f'{protocol}://{domain}/payments/success/',
                cancel_url=f'{protocol}://{domain}/payments/cancelled/',
                payment_method_types=['card'],
                mode='payment',
                # TODO: Product implementation
                line_items=[
                    {
                        'quantity': 1,
                        'price_data': {
                            'currency': 'pln',
                            'unit_amount': int(product_price * 100),
                            'product_data': {
                                'name': 'T-shirt',
                            },
                        },
                    }
                ]
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})
    return JsonResponse({'error': 'Invalid request method'}, status=400)


@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except (stripe.error.SignatureVerificationError, ValueError):
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        print("Payment was successful.")
        # TODO: run some custom code here

    return HttpResponse(status=200)


class SuccessView(TemplateView):
    template_name = 'payments/success.html'


class CancelledView(TemplateView):
    template_name = 'payments/cancelled.html'
